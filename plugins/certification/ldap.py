import logging
import os
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

# Cache for LDAP lookups
_ldap_cache = {}
# Cache for Mattermost handle to email mapping
mattermost_email_cache: dict[str, str] = {}


def get_email_from_mattermost_handle_api(mattermost_handle: str) -> Optional[str]:
    """
    Get email address from Mattermost handle using Mattermost API
    Results are cached to avoid duplicate requests
    """
    if not all([mattermost_token, mattermost_base_url]):
        logger.warning("Mattermost API configuration incomplete")
        return None

    # Check cache first
    if mattermost_handle in mattermost_email_cache:
        return mattermost_email_cache[mattermost_handle]

    try:
        user_details = get_user_by_name(
            mattermost_token, mattermost_base_url, mattermost_handle
        )
        email = user_details.get("email")

        if email:
            # Cache the result
            mattermost_email_cache[mattermost_handle] = email
            logger.info(
                f"Found email {email} for Mattermost handle {mattermost_handle}"
            )
            return email
        else:
            logger.warning(f"No email found for Mattermost handle {mattermost_handle}")
    except Exception as e:
        logger.error(
            f"Failed to get email for Mattermost handle {mattermost_handle}: {str(e)}"
        )

    # Cache negative result
    mattermost_email_cache[mattermost_handle] = None
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

    # Check cache first
    if handle in _ldap_cache:
        return _ldap_cache[handle]

    # Get email from Mattermost API
    email = get_email_from_mattermost_handle_api(handle)
    if not email:
        logger.warning(f"Could not get email for Mattermost handle {handle}")
        _ldap_cache[handle] = None
        return None

    try:
        # Connect to LDAP server
        server = ldap3.Server(LDAP_SERVER, use_ssl=True)
        conn = ldap3.Connection(
            server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True
        )

        # Search for user by email from Mattermost API
        search_filter = f"(mail={email})"
        logger.debug(f"Searching LDAP with filter: {search_filter}")

        conn.search(
            search_base=LDAP_BASE_DN,
            search_filter=search_filter,
            attributes=["*"],  # Get all attributes to see what's available
        )

        logger.debug(f"Search returned {len(conn.entries)} entries")

        if conn.entries:
            entry = conn.entries[0]
            logger.debug(f"Entry DN: {entry.entry_dn}")
            logger.debug(
                f"Available attribute keys: {list(entry.entry_attributes_as_dict.keys())}"
            )

            # Log all attribute values for debugging
            logger.info(f"All LDAP attributes for {handle} (email: {email}):")
            for attr_name, attr_values in entry.entry_attributes_as_dict.items():
                if attr_name.lower() != "jpegphoto":  # Skip binary photo data
                    logger.info(f"  {attr_name}: {attr_values}")

            github_username = (
                entry.gitHubID.value if hasattr(entry, "gitHubID") else None
            )

            if github_username:
                # Cache the result
                _ldap_cache[handle] = github_username
                logger.info(
                    f"Found GitHub username {github_username} for Mattermost handle {handle}"
                )
                return github_username
            else:
                logger.debug("No githubUsername attribute found in this entry")

        # Cache negative result
        _ldap_cache[handle] = None
        logger.info(f"No GitHub username found for Mattermost handle {handle}")
        return None

    except Exception as e:
        logger.error(f"LDAP lookup failed for {handle}: {str(e)}")
        # Cache negative result to avoid repeated failed lookups
        _ldap_cache[handle] = None
        return None
    finally:
        if "conn" in locals():
            conn.unbind()


def get_email_from_github_username(github_username: str) -> Optional[str]:
    """
    Get email address from GitHub username using LDAP lookup by GitHubID attribute
    """
    if not all([LDAP_SERVER, LDAP_BASE_DN, LDAP_BIND_DN, LDAP_BIND_PASSWORD]):
        logger.warning("LDAP configuration incomplete")
        return None

    try:
        # Connect to LDAP server
        server = ldap3.Server(LDAP_SERVER, use_ssl=True)
        conn = ldap3.Connection(
            server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True
        )

        # Search for user by GitHub username using GitHubID attribute
        search_filter = f"(gitHubID={github_username})"
        logger.debug(f"Searching LDAP with filter: {search_filter}")

        conn.search(
            search_base=LDAP_BASE_DN,
            search_filter=search_filter,
            attributes=["mail", "gitHubID"],
        )

        logger.debug(f"Search returned {len(conn.entries)} entries")

        if conn.entries:
            entry = conn.entries[0]
            email = entry.mail.value if hasattr(entry, "mail") else None

            if email:
                logger.info(
                    f"Found email {email} for GitHub username {github_username}"
                )
                return email
            else:
                logger.warning(f"No email found for GitHub username {github_username}")
        else:
            logger.info(f"No LDAP entry found for GitHub username {github_username}")

        return None

    except Exception as e:
        logger.error(
            f"LDAP lookup failed for GitHub username {github_username}: {str(e)}"
        )
        return None
    finally:
        if "conn" in locals():
            conn.unbind()


def get_mattermost_handle_from_github_username(github_username: str) -> Optional[str]:
    """
    Get Mattermost handle from GitHub username
    Flow: GitHub username -> LDAP (email) -> Mattermost API (handle)
    """
    # Get email from LDAP using GitHub username
    email = get_email_from_github_username(github_username)
    if not email:
        logger.warning(f"Could not find email for GitHub username {github_username}")
        return None

    # Get Mattermost handle using email
    if not all([mattermost_token, mattermost_base_url]):
        logger.warning("Mattermost API configuration incomplete")
        return None

    mattermost_handle = get_mattermost_handle_by_email(
        mattermost_token, mattermost_base_url, email
    )
    if mattermost_handle:
        logger.info(
            f"Found Mattermost handle {mattermost_handle} for GitHub username {github_username}"
        )
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
