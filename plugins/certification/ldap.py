import contextlib
import logging
import os
import socket
import threading
import urllib.parse
from collections.abc import Iterator
from typing import Optional

import ldap3
from mattermost_api import (
    get_mattermost_handle_by_email,
    get_user_by_name,
    mattermost_base_url,
    mattermost_token,
)

logger = logging.getLogger(__name__)

LDAP_SERVER = os.environ.get("LDAP_SERVER")
LDAP_BASE_DN = os.environ.get("LDAP_BASE_DN")
LDAP_BIND_DN = os.environ.get("LDAP_BIND_DN")
LDAP_BIND_PASSWORD = os.environ.get("LDAP_BIND_PASSWORD")
HTTPS_PROXY = os.environ.get("HTTPS_PROXY")

_proxy_patch_lock = threading.Lock()


@contextlib.contextmanager
def _ldap_connect() -> Iterator[ldap3.Connection]:
    """Open an authenticated LDAP connection, yielding it for use within the context.

    If HTTPS_PROXY is set, tunnels the connection through the proxy via HTTP CONNECT
    (ldap3 does not natively support proxies, so socket.socket is patched temporarily).
    The lock ensures the patch is thread-safe.
    """
    server = ldap3.Server(LDAP_SERVER, use_ssl=True)

    if HTTPS_PROXY:
        parsed = urllib.parse.urlparse(HTTPS_PROXY)
        proxy_host = parsed.hostname
        proxy_port = parsed.port or 3128
        _original_socket = socket.socket

        class _ProxiedSocket(_original_socket):
            def connect(self, address):
                # Only intercept LDAPS connections (port 636)
                if isinstance(address, tuple) and len(address) >= 2 and address[1] == 636:
                    super().connect((proxy_host, proxy_port))
                    req = (
                        f"CONNECT {address[0]}:{address[1]} HTTP/1.1\r\n"
                        f"Host: {address[0]}:{address[1]}\r\n\r\n"
                    )
                    self.sendall(req.encode())
                    resp = b""
                    while b"\r\n\r\n" not in resp:
                        chunk = self.recv(4096)
                        if not chunk:
                            break
                        resp += chunk
                    if b" 200 " not in resp:
                        raise ConnectionError(f"Proxy CONNECT failed: {resp!r}")
                else:
                    super().connect(address)

        with _proxy_patch_lock:
            socket.socket = _ProxiedSocket
            try:
                conn = ldap3.Connection(
                    server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True
                )
            finally:
                socket.socket = _original_socket
    else:
        conn = ldap3.Connection(
            server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True
        )

    try:
        yield conn
    finally:
        conn.unbind()

_ldap_cache: dict[str, Optional[str]] = {}
_mattermost_email_cache: dict[str, Optional[str]] = {}


def get_email_from_mattermost_handle_api(mattermost_handle: str) -> Optional[str]:
    """
    Get email address from Mattermost handle using Mattermost API
    Results are cached to avoid duplicate requests
    """
    if not all([mattermost_token, mattermost_base_url]):
        logger.warning("Mattermost API configuration incomplete")
        return None

    if mattermost_handle in _mattermost_email_cache:
        return _mattermost_email_cache[mattermost_handle]

    try:
        user_details = get_user_by_name(
            mattermost_token, mattermost_base_url, mattermost_handle
        )
        email = user_details.get("email")

        if email:
            # Cache the result
            _mattermost_email_cache[mattermost_handle] = email
            return email
        else:
            logger.warning(f"No email found for Mattermost handle {mattermost_handle}")
    except Exception as e:
        logger.error(
            f"Failed to get email for Mattermost handle {mattermost_handle}: {str(e)}"
        )

    # Cache negative result
    _mattermost_email_cache[mattermost_handle] = None
    return None


def get_github_username_from_mattermost_handle(handle: str) -> Optional[str]:
    """
    Get GitHub username from Mattermost handle using LDAP lookup
    First gets email from Mattermost API, then searches LDAP by email
    Results are cached to avoid duplicate requests
    """
    if not all([LDAP_SERVER, LDAP_BASE_DN, LDAP_BIND_DN, LDAP_BIND_PASSWORD]):
        logger.warning("LDAP configuration incomplete")
        return None

    if handle in _ldap_cache:
        return _ldap_cache[handle]

    email = get_email_from_mattermost_handle_api(handle)
    if not email:
        logger.warning(f"Could not get email for Mattermost handle {handle}")
        _ldap_cache[handle] = None
        return None

    try:
        with _ldap_connect() as conn:
            conn.search(
                search_base=LDAP_BASE_DN,
                search_filter=f"(mail={email})",
                attributes=["*"],
            )

            if conn.entries:
                entry = conn.entries[0]
                github_username = (
                    entry.gitHubID.value if hasattr(entry, "gitHubID") else None
                )
                if github_username:
                    _ldap_cache[handle] = github_username
                    return github_username
                else:
                    logger.warning(f"No GitHub username (gitHubID) found in LDAP for {handle}")

        # Cache negative result
        _ldap_cache[handle] = None
        return None

    except Exception as e:
        logger.error(f"LDAP lookup failed for {handle}: {str(e)}")
        # Cache negative result to avoid repeated failed lookups
        _ldap_cache[handle] = None
        return None


def get_email_from_github_username(github_username: str) -> Optional[str]:
    """
    Get email address from GitHub username using LDAP lookup by GitHubID attribute
    """
    if not all([LDAP_SERVER, LDAP_BASE_DN, LDAP_BIND_DN, LDAP_BIND_PASSWORD]):
        logger.warning("LDAP configuration incomplete")
        return None

    try:
        with _ldap_connect() as conn:
            conn.search(
                search_base=LDAP_BASE_DN,
                search_filter=f"(gitHubID={github_username})",
                attributes=["mail", "gitHubID"],
            )

            if conn.entries:
                entry = conn.entries[0]
                email = entry.mail.value if hasattr(entry, "mail") else None
                if email:
                    return email
                else:
                    logger.warning(f"No email found for GitHub username {github_username}")
            else:
                logger.warning(f"No LDAP entry found for GitHub username {github_username}")

        return None

    except Exception as e:
        logger.error(
            f"LDAP lookup failed for GitHub username {github_username}: {str(e)}"
        )
        return None


def get_mattermost_handle_from_github_username(github_username: str) -> Optional[str]:
    """
    Get Mattermost handle from GitHub username
    Flow: GitHub username -> LDAP (email) -> Mattermost API (handle)
    """
    email = get_email_from_github_username(github_username)
    if not email:
        logger.warning(f"Could not find email for GitHub username {github_username}")
        return None

    if not all([mattermost_token, mattermost_base_url]):
        logger.warning("Mattermost API configuration incomplete")
        return None

    mattermost_handle = get_mattermost_handle_by_email(
        mattermost_token, mattermost_base_url, email
    )
    if mattermost_handle:
        return mattermost_handle
    else:
        logger.warning(
            f"Could not find Mattermost handle for email {email} (GitHub user: {github_username})"
        )
        return None


def get_email_from_mattermost_handle(mattermost_handle: str) -> Optional[str]:
    """
    Get email address from Mattermost handle using Mattermost API
    This is now a wrapper around the API-based function for compatibility
    """
    return get_email_from_mattermost_handle_api(mattermost_handle)
