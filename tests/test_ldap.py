#!/usr/bin/env python3
"""
Tests for plugins/certification/ldap.py

Covers:
  - _ldap_connect: no-proxy path
  - _ldap_connect: HTTP CONNECT proxy path (socket patch applied and restored)
  - _ldap_connect: proxy CONNECT rejection raises ConnectionError
  - _ldap_connect: non-636 connections are NOT proxied
  - get_github_username_from_mattermost_handle: hit / miss / incomplete config / no email
  - get_email_from_github_username: hit / miss / incomplete config
"""

import os
import socket
import sys
import threading
import unittest
from unittest.mock import MagicMock, call, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ldap3

# ---------------------------------------------------------------------------
# Module-level env var setup must happen BEFORE importing the module under test
# so that the module-level constants (LDAP_SERVER, HTTPS_PROXY, …) are set.
# ---------------------------------------------------------------------------
LDAP_ENV = {
    "LDAP_SERVER": "ldap.canonical.com",
    "LDAP_BASE_DN": "ou=staff,dc=canonical,dc=com",
    "LDAP_BIND_DN": "cn=errbot,dc=canonical,dc=com",
    "LDAP_BIND_PASSWORD": "secret",
}


def _import_ldap_module(extra_env=None):
    """Import (or re-import) the ldap module with controlled env vars."""
    import importlib
    import plugins.certification.ldap as mod

    env = {**LDAP_ENV, **(extra_env or {})}
    # Patch the module-level constants directly so we don't need to reload
    mod.LDAP_SERVER = env.get("LDAP_SERVER")
    mod.LDAP_BASE_DN = env.get("LDAP_BASE_DN")
    mod.LDAP_BIND_DN = env.get("LDAP_BIND_DN")
    mod.LDAP_BIND_PASSWORD = env.get("LDAP_BIND_PASSWORD")
    mod.HTTPS_PROXY = env.get("HTTPS_PROXY")
    return mod


class TestLdapConnect(unittest.TestCase):
    """Tests for the _ldap_connect context manager."""

    def _make_mock_conn(self):
        conn = MagicMock()
        conn.entries = []
        return conn

    # ------------------------------------------------------------------
    # No-proxy path
    # ------------------------------------------------------------------
    @patch("plugins.certification.ldap.ldap3.Connection")
    @patch("plugins.certification.ldap.ldap3.Server")
    def test_no_proxy_creates_direct_connection(self, mock_server, mock_conn_cls):
        """Without HTTPS_PROXY, ldap3.Connection is called directly."""
        import plugins.certification.ldap as mod
        mod.HTTPS_PROXY = None
        mock_conn = self._make_mock_conn()
        mock_conn_cls.return_value = mock_conn

        with mod._ldap_connect() as conn:
            self.assertIs(conn, mock_conn)

        mock_server.assert_called_once_with(mod.LDAP_SERVER, use_ssl=True)
        mock_conn_cls.assert_called_once()
        mock_conn.unbind.assert_called_once()

    @patch("plugins.certification.ldap.ldap3.Connection")
    @patch("plugins.certification.ldap.ldap3.Server")
    def test_no_proxy_unbinds_on_exception(self, mock_server, mock_conn_cls):
        """unbind() is called even when the body raises."""
        import plugins.certification.ldap as mod
        mod.HTTPS_PROXY = None
        mock_conn = self._make_mock_conn()
        mock_conn_cls.return_value = mock_conn

        with self.assertRaises(RuntimeError):
            with mod._ldap_connect():
                raise RuntimeError("body error")

        mock_conn.unbind.assert_called_once()

    # ------------------------------------------------------------------
    # Proxy path — happy path
    # ------------------------------------------------------------------
    @patch("plugins.certification.ldap.ldap3.Connection")
    @patch("plugins.certification.ldap.ldap3.Server")
    def test_proxy_patches_socket_and_restores(self, mock_server, mock_conn_cls):
        """With HTTPS_PROXY set, socket.socket is patched during Connection()
        creation and restored immediately after, before yielding."""
        import plugins.certification.ldap as mod
        mod.HTTPS_PROXY = "http://proxy.internal:3128"
        mock_conn = self._make_mock_conn()

        captured_socket_during = {}

        def capture_conn(*args, **kwargs):
            captured_socket_during["cls"] = socket.socket
            return mock_conn

        mock_conn_cls.side_effect = capture_conn
        original_socket = socket.socket

        with mod._ldap_connect():
            # After connection is established the patch must already be removed
            self.assertIs(socket.socket, original_socket)

        # The class used during Connection() must have been our proxy subclass
        self.assertIsNot(captured_socket_during["cls"], original_socket)
        # And it must be restored afterwards
        self.assertIs(socket.socket, original_socket)

    @patch("plugins.certification.ldap.ldap3.Connection")
    @patch("plugins.certification.ldap.ldap3.Server")
    def test_proxy_socket_restored_on_connection_error(self, mock_server, mock_conn_cls):
        """socket.socket is restored even when ldap3.Connection() raises."""
        import plugins.certification.ldap as mod
        mod.HTTPS_PROXY = "http://proxy.internal:3128"
        mock_conn_cls.side_effect = ldap3.core.exceptions.LDAPException("connect fail")
        original_socket = socket.socket

        with self.assertRaises(ldap3.core.exceptions.LDAPException):
            with mod._ldap_connect():
                pass

        self.assertIs(socket.socket, original_socket)

    # ------------------------------------------------------------------
    # Proxy socket: CONNECT handshake
    # ------------------------------------------------------------------
    def test_proxied_socket_sends_connect_and_succeeds(self):
        """_ProxiedSocket.connect sends HTTP CONNECT for port 636 and reads 200."""
        import plugins.certification.ldap as mod
        mod.HTTPS_PROXY = "http://proxy.internal:3128"

        # Build the _ProxiedSocket class by peeking inside _ldap_connect
        proxy_socket_cls = None
        original_socket = socket.socket

        with patch("plugins.certification.ldap.ldap3.Connection") as mock_conn_cls, \
             patch("plugins.certification.ldap.ldap3.Server"):
            mock_conn = self._make_mock_conn()

            def capture_and_return(*a, **kw):
                nonlocal proxy_socket_cls
                proxy_socket_cls = socket.socket  # captured while patched
                return mock_conn

            mock_conn_cls.side_effect = capture_and_return
            with mod._ldap_connect():
                pass

        self.assertIsNotNone(proxy_socket_cls)

        # Now test the proxied socket directly
        instance = proxy_socket_cls.__new__(proxy_socket_cls)
        original_socket.__init__(instance)

        sent_data = []
        received_response = [b"HTTP/1.1 200 Connection established\r\n\r\n"]

        with patch.object(original_socket, "connect", autospec=True) as mock_connect, \
             patch.object(original_socket, "sendall", autospec=True,
                          side_effect=lambda d: sent_data.append(d)), \
             patch.object(original_socket, "recv", autospec=True,
                          side_effect=lambda n: received_response.pop(0) if received_response else b""):
            instance.connect(("93.184.216.34", 636))

        mock_connect.assert_called_once_with(("proxy.internal", 3128))
        self.assertTrue(any(b"CONNECT 93.184.216.34:636 HTTP/1.1" in d for d in sent_data))

    def test_proxied_socket_raises_on_connect_rejection(self):
        """_ProxiedSocket.connect raises ConnectionError when proxy returns non-200."""
        import plugins.certification.ldap as mod
        mod.HTTPS_PROXY = "http://proxy.internal:3128"

        proxy_socket_cls = None
        original_socket = socket.socket

        with patch("plugins.certification.ldap.ldap3.Connection") as mock_conn_cls, \
             patch("plugins.certification.ldap.ldap3.Server"):
            mock_conn = self._make_mock_conn()

            def capture_and_return(*a, **kw):
                nonlocal proxy_socket_cls
                proxy_socket_cls = socket.socket
                return mock_conn

            mock_conn_cls.side_effect = capture_and_return
            with mod._ldap_connect():
                pass

        instance = proxy_socket_cls.__new__(proxy_socket_cls)
        original_socket.__init__(instance)

        with patch.object(original_socket, "connect", autospec=True), \
             patch.object(original_socket, "sendall", autospec=True), \
             patch.object(original_socket, "recv", autospec=True,
                          return_value=b"HTTP/1.1 403 Forbidden\r\n\r\n"):
            with self.assertRaises(ConnectionError) as ctx:
                instance.connect(("93.184.216.34", 636))

        self.assertIn("Proxy CONNECT failed", str(ctx.exception))

    def test_proxied_socket_does_not_intercept_non_636(self):
        """_ProxiedSocket.connect passes through addresses on ports other than 636."""
        import plugins.certification.ldap as mod
        mod.HTTPS_PROXY = "http://proxy.internal:3128"

        proxy_socket_cls = None
        original_socket = socket.socket

        with patch("plugins.certification.ldap.ldap3.Connection") as mock_conn_cls, \
             patch("plugins.certification.ldap.ldap3.Server"):
            mock_conn = self._make_mock_conn()

            def capture_and_return(*a, **kw):
                nonlocal proxy_socket_cls
                proxy_socket_cls = socket.socket
                return mock_conn

            mock_conn_cls.side_effect = capture_and_return
            with mod._ldap_connect():
                pass

        instance = proxy_socket_cls.__new__(proxy_socket_cls)
        original_socket.__init__(instance)

        with patch.object(original_socket, "connect", autospec=True) as mock_connect, \
             patch.object(original_socket, "sendall", autospec=True) as mock_sendall:
            instance.connect(("10.0.0.1", 443))

        # Should have called super().connect with the original address, not the proxy
        mock_connect.assert_called_once_with(("10.0.0.1", 443))
        mock_sendall.assert_not_called()


class TestGetGithubUsernameFromMattermostHandle(unittest.TestCase):
    """Tests for get_github_username_from_mattermost_handle."""

    def setUp(self):
        import plugins.certification.ldap as mod
        mod.LDAP_SERVER = LDAP_ENV["LDAP_SERVER"]
        mod.LDAP_BASE_DN = LDAP_ENV["LDAP_BASE_DN"]
        mod.LDAP_BIND_DN = LDAP_ENV["LDAP_BIND_DN"]
        mod.LDAP_BIND_PASSWORD = LDAP_ENV["LDAP_BIND_PASSWORD"]
        mod.HTTPS_PROXY = None
        mod._ldap_cache.clear()
        mod._mattermost_email_cache.clear()
        self.mod = mod

    def _mock_ldap_conn(self, entries=None):
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        conn.entries = entries or []
        return conn

    @patch("plugins.certification.ldap.get_email_from_mattermost_handle_api")
    @patch("plugins.certification.ldap._ldap_connect")
    def test_returns_github_username_on_hit(self, mock_connect, mock_get_email):
        """Returns gitHubID when LDAP search finds a matching entry."""
        mock_get_email.return_value = "user@canonical.com"
        entry = MagicMock()
        entry.gitHubID.value = "gh-user"
        conn = self._mock_ldap_conn(entries=[entry])
        mock_connect.return_value = conn

        result = self.mod.get_github_username_from_mattermost_handle("matthandle")

        self.assertEqual(result, "gh-user")
        self.assertEqual(self.mod._ldap_cache["matthandle"], "gh-user")

    @patch("plugins.certification.ldap.get_email_from_mattermost_handle_api")
    @patch("plugins.certification.ldap._ldap_connect")
    def test_returns_none_when_no_entries(self, mock_connect, mock_get_email):
        """Returns None when LDAP search returns no entries."""
        mock_get_email.return_value = "user@canonical.com"
        conn = self._mock_ldap_conn(entries=[])
        mock_connect.return_value = conn

        result = self.mod.get_github_username_from_mattermost_handle("matthandle")

        self.assertIsNone(result)
        self.assertIsNone(self.mod._ldap_cache["matthandle"])

    @patch("plugins.certification.ldap.get_email_from_mattermost_handle_api")
    def test_returns_none_when_no_email(self, mock_get_email):
        """Returns None immediately when Mattermost API returns no email."""
        mock_get_email.return_value = None

        result = self.mod.get_github_username_from_mattermost_handle("matthandle")

        self.assertIsNone(result)
        self.assertIsNone(self.mod._ldap_cache["matthandle"])

    def test_returns_none_when_config_incomplete(self):
        """Returns None immediately when LDAP env vars are missing."""
        self.mod.LDAP_SERVER = None

        result = self.mod.get_github_username_from_mattermost_handle("matthandle")

        self.assertIsNone(result)

    @patch("plugins.certification.ldap.get_email_from_mattermost_handle_api")
    @patch("plugins.certification.ldap._ldap_connect")
    def test_uses_cache_on_second_call(self, mock_connect, mock_get_email):
        """Second call for the same handle uses cache; LDAP is not hit again."""
        mock_get_email.return_value = "user@canonical.com"
        entry = MagicMock()
        entry.gitHubID.value = "gh-user"
        conn = self._mock_ldap_conn(entries=[entry])
        mock_connect.return_value = conn

        self.mod.get_github_username_from_mattermost_handle("matthandle")
        self.mod.get_github_username_from_mattermost_handle("matthandle")

        mock_connect.assert_called_once()

    @patch("plugins.certification.ldap.get_email_from_mattermost_handle_api")
    @patch("plugins.certification.ldap._ldap_connect")
    def test_caches_negative_result_on_ldap_error(self, mock_connect, mock_get_email):
        """LDAP errors are caught, negative result is cached."""
        mock_get_email.return_value = "user@canonical.com"
        mock_connect.side_effect = Exception("connection refused")

        result = self.mod.get_github_username_from_mattermost_handle("matthandle")

        self.assertIsNone(result)
        self.assertIn("matthandle", self.mod._ldap_cache)


class TestGetEmailFromGithubUsername(unittest.TestCase):
    """Tests for get_email_from_github_username."""

    def setUp(self):
        import plugins.certification.ldap as mod
        mod.LDAP_SERVER = LDAP_ENV["LDAP_SERVER"]
        mod.LDAP_BASE_DN = LDAP_ENV["LDAP_BASE_DN"]
        mod.LDAP_BIND_DN = LDAP_ENV["LDAP_BIND_DN"]
        mod.LDAP_BIND_PASSWORD = LDAP_ENV["LDAP_BIND_PASSWORD"]
        mod.HTTPS_PROXY = None
        mod._ldap_cache.clear()
        self.mod = mod

    def _mock_ldap_conn(self, entries=None):
        conn = MagicMock()
        conn.__enter__ = MagicMock(return_value=conn)
        conn.__exit__ = MagicMock(return_value=False)
        conn.entries = entries or []
        return conn

    @patch("plugins.certification.ldap._ldap_connect")
    def test_returns_email_on_hit(self, mock_connect):
        """Returns mail attribute when LDAP finds the GitHub user."""
        entry = MagicMock()
        entry.mail.value = "gh@canonical.com"
        conn = self._mock_ldap_conn(entries=[entry])
        mock_connect.return_value = conn

        result = self.mod.get_email_from_github_username("gh-user")

        self.assertEqual(result, "gh@canonical.com")

    @patch("plugins.certification.ldap._ldap_connect")
    def test_returns_none_when_no_entries(self, mock_connect):
        """Returns None when no LDAP entry matches the GitHub username."""
        conn = self._mock_ldap_conn(entries=[])
        mock_connect.return_value = conn

        result = self.mod.get_email_from_github_username("unknown-gh-user")

        self.assertIsNone(result)

    def test_returns_none_when_config_incomplete(self):
        """Returns None immediately when LDAP env vars are missing."""
        self.mod.LDAP_BASE_DN = None

        result = self.mod.get_email_from_github_username("gh-user")

        self.assertIsNone(result)

    @patch("plugins.certification.ldap._ldap_connect")
    def test_returns_none_on_ldap_error(self, mock_connect):
        """LDAP errors are caught and None is returned."""
        mock_connect.side_effect = Exception("timeout")

        result = self.mod.get_email_from_github_username("gh-user")

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
