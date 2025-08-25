#!/usr/bin/env python3
"""
Test for the PullRequestCache get_team_members method with mocked GitHub connectivity
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from unittest.mock import MagicMock, patch

from plugins.certification.pr_cache import PullRequestCache


class TestPRCacheTeamMembers(unittest.TestCase):
    """Test cases for PR cache get_team_members functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.pr_cache = PullRequestCache(
            repo_filter=["repo1", "repo2"],
            github_token="test-token",
            github_org="test-org"
        )

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_success(self, mock_get):
        """Test successful retrieval of team members"""
        # Mock response with team members
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            page = kwargs.get("params", {}).get("page", 1)
            
            if "teams/test-team/members" in url:
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {"login": "user1"},
                        {"login": "user2"},
                        {"login": "user3"}
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = []
            
            return mock_response

        mock_get.side_effect = side_effect

        # Execute get_team_members
        members = self.pr_cache.get_team_members("test-team")

        # Assertions
        self.assertEqual(len(members), 3)
        self.assertIn("user1", members)
        self.assertIn("user2", members)
        self.assertIn("user3", members)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_with_pagination(self, mock_get):
        """Test get_team_members handles pagination correctly"""
        # Mock response with multiple pages
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            page = kwargs.get("params", {}).get("page", 1)
            
            if "teams/large-team/members" in url:
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {"login": f"user{i}"} for i in range(1, 101)  # 100 members
                    ]
                elif page == 2:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {"login": f"user{i}"} for i in range(101, 151)  # 50 more members
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = []
            
            return mock_response

        mock_get.side_effect = side_effect

        # Execute get_team_members
        members = self.pr_cache.get_team_members("large-team")

        # Assertions
        self.assertEqual(len(members), 150)
        self.assertIn("user1", members)
        self.assertIn("user100", members)
        self.assertIn("user150", members)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_handles_404(self, mock_get):
        """Test that get_team_members returns empty list for non-existent team"""
        # Mock 404 response
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "Not Found"}
        mock_get.return_value = mock_response

        # Execute get_team_members
        members = self.pr_cache.get_team_members("non-existent-team")

        # Assertions
        self.assertEqual(members, [])

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_handles_request_exception(self, mock_get):
        """Test that get_team_members handles network errors gracefully"""
        import requests
        
        # Mock network error
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Execute get_team_members
        members = self.pr_cache.get_team_members("test-team")

        # Assertions
        self.assertEqual(members, [])

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_handles_other_http_errors(self, mock_get):
        """Test that get_team_members handles other HTTP errors"""
        import requests
        
        # Mock 500 error - raise_for_status will be called and should raise
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("Internal Server Error")
        mock_get.return_value = mock_response

        # Execute get_team_members
        members = self.pr_cache.get_team_members("test-team")

        # Assertions - should return empty list due to exception handling
        self.assertEqual(members, [])

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_with_empty_team_name(self, mock_get):
        """Test that get_team_members returns empty list for empty team name"""
        # No need to mock since it should return early
        mock_get.return_value = MagicMock()
        
        # Execute get_team_members with empty string
        members = self.pr_cache.get_team_members("")

        # Assertions
        self.assertEqual(members, [])
        # Verify no API call was made since empty string should be caught
        mock_get.assert_not_called()

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_headers_contain_token(self, mock_get):
        """Test that get_team_members includes authentication token in headers"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Execute get_team_members
        self.pr_cache.get_team_members("test-team")

        # Verify headers were passed correctly
        mock_get.assert_called()
        call_args = mock_get.call_args
        headers = call_args[1]["headers"]
        self.assertEqual(headers["Authorization"], "token test-token")
        self.assertEqual(headers["Accept"], "application/vnd.github.v3+json")

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_uses_correct_url(self, mock_get):
        """Test that get_team_members constructs the correct GitHub API URL"""
        # Mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # Execute get_team_members
        self.pr_cache.get_team_members("my-team")

        # Verify correct URL was called
        mock_get.assert_called()
        call_args = mock_get.call_args
        url = call_args[0][0]
        self.assertEqual(url, "https://api.github.com/orgs/test-org/teams/my-team/members")

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_team_members_mixed_case_usernames(self, mock_get):
        """Test that get_team_members preserves username case"""
        # Mock response with mixed case usernames - handle pagination
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            page = kwargs.get("params", {}).get("page", 1)
            
            if page == 1:
                mock_response.status_code = 200
                mock_response.json.return_value = [
                    {"login": "UserOne"},
                    {"login": "user-two"},
                    {"login": "USER_THREE"}
                ]
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = []  # Empty for subsequent pages
            
            return mock_response
        
        mock_get.side_effect = side_effect

        # Execute get_team_members
        members = self.pr_cache.get_team_members("test-team")

        # Assertions - verify case is preserved
        self.assertEqual(len(members), 3)
        self.assertIn("UserOne", members)
        self.assertIn("user-two", members)
        self.assertIn("USER_THREE", members)


if __name__ == "__main__":
    unittest.main()