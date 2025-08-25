#!/usr/bin/env python3
"""
Test for the new "changes requested" PR functionality
"""

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from plugins.certification.pr_cache import PullRequestCache


class TestPRChangesRequested(unittest.TestCase):
    """Test cases for PR changes requested functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.pr_cache = PullRequestCache(
            repo_filter=["test-repo"], github_token="test-token", github_org="test-org"
        )

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_prs_for_user_with_changes_requested(self, mock_get):
        """Test that get_prs_for_user correctly identifies PRs with changes requested"""
        # Set up cache with a PR authored by the user
        self.pr_cache.cache = {
            "test-repo": [
                {
                    "number": 123,
                    "title": "Test PR",
                    "user": {"login": "test-author"},
                    "requested_reviewers": [{"login": "reviewer1"}],
                    "requested_teams": [],
                    "assignees": []
                }
            ]
        }
        self.pr_cache.last_updated = datetime.now()
        
        # Mock review API response with changes requested
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"state": "COMMENTED", "user": {"login": "reviewer1"}},
            {"state": "CHANGES_REQUESTED", "user": {"login": "reviewer2"}},
        ]
        mock_get.return_value = mock_response

        result = self.pr_cache.get_prs_for_user("test-author")

        # PR should be in changes_requested category
        self.assertEqual(len(result["authored_changes_requested"]), 1)
        self.assertEqual(result["authored_changes_requested"][0]["number"], 123)
        # Should not be in other categories
        self.assertEqual(len(result["authored_approved"]), 0)
        self.assertEqual(len(result["authored_pending_review"]), 0)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_prs_for_user_with_approvals(self, mock_get):
        """Test that get_prs_for_user correctly identifies PRs with approvals"""
        # Set up cache with a PR authored by the user
        self.pr_cache.cache = {
            "test-repo": [
                {
                    "number": 456,
                    "title": "Approved PR",
                    "user": {"login": "test-author"},
                    "requested_reviewers": [],
                    "requested_teams": [],
                    "assignees": [{"login": "assignee1"}]
                }
            ]
        }
        self.pr_cache.last_updated = datetime.now()
        
        # Mock review API response with approval
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"state": "COMMENTED", "user": {"login": "reviewer1"}},
            {"state": "APPROVED", "user": {"login": "reviewer2"}},
        ]
        mock_get.return_value = mock_response

        result = self.pr_cache.get_prs_for_user("test-author")

        # PR should be in approved category
        self.assertEqual(len(result["authored_approved"]), 1)
        self.assertEqual(result["authored_approved"][0]["number"], 456)
        # Should not be in other categories
        self.assertEqual(len(result["authored_changes_requested"]), 0)
        self.assertEqual(len(result["authored_pending_review"]), 0)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_prs_for_user_with_both_approval_and_changes(self, mock_get):
        """Test that get_prs_for_user handles PRs with both approvals and changes requested"""
        # Set up cache with a PR authored by the user
        self.pr_cache.cache = {
            "test-repo": [
                {
                    "number": 789,
                    "title": "Mixed Review PR",
                    "user": {"login": "test-author"},
                    "requested_reviewers": [{"login": "reviewer3"}],
                    "requested_teams": [],
                    "assignees": []
                }
            ]
        }
        self.pr_cache.last_updated = datetime.now()
        
        # Mock review API response with both approved and changes requested
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"state": "APPROVED", "user": {"login": "reviewer1"}},
            {"state": "CHANGES_REQUESTED", "user": {"login": "reviewer2"}},
        ]
        mock_get.return_value = mock_response

        result = self.pr_cache.get_prs_for_user("test-author")

        # PR should be in changes_requested category (takes precedence over approval)
        self.assertEqual(len(result["authored_changes_requested"]), 1)
        self.assertEqual(result["authored_changes_requested"][0]["number"], 789)
        # Should not be in approved category
        self.assertEqual(len(result["authored_approved"]), 0)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_prs_for_user_with_review_api_error(self, mock_get):
        """Test that get_prs_for_user handles review API errors gracefully"""
        # Set up cache with a PR authored by the user
        self.pr_cache.cache = {
            "test-repo": [
                {
                    "number": 500,
                    "title": "Error PR",
                    "user": {"login": "test-author"},
                    "requested_reviewers": [{"login": "reviewer1"}],
                    "requested_teams": [],
                    "assignees": [],
                }
            ]
        }
        self.pr_cache.last_updated = datetime.now()

        # Mock a failed review API response (500 error)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = self.pr_cache.get_prs_for_user("test-author")

        # PR should be in unknown_status category when API fails
        self.assertEqual(len(result["authored_unknown_status"]), 1)
        self.assertEqual(result["authored_unknown_status"][0]["number"], 500)
        # Should not be in other categories
        self.assertEqual(len(result["authored_changes_requested"]), 0)
        self.assertEqual(len(result["authored_approved"]), 0)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_prs_for_user_with_network_error(self, mock_get):
        """Test that get_prs_for_user handles network errors gracefully"""
        import requests
        
        # Set up cache with a PR authored by the user
        self.pr_cache.cache = {
            "test-repo": [
                {
                    "number": 503,
                    "title": "Network Error PR",
                    "user": {"login": "test-author"},
                    "requested_reviewers": [{"login": "reviewer1"}],
                    "requested_teams": [],
                    "assignees": [],
                }
            ]
        }
        self.pr_cache.last_updated = datetime.now()
        
        # Mock a network exception
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = self.pr_cache.get_prs_for_user("test-author")

        # PR should be in unknown_status category when network fails
        self.assertEqual(len(result["authored_unknown_status"]), 1)
        self.assertEqual(result["authored_unknown_status"][0]["number"], 503)
        # Should not be in other categories
        self.assertEqual(len(result["authored_changes_requested"]), 0)
        self.assertEqual(len(result["authored_approved"]), 0)

    def test_get_prs_for_user_returns_changes_requested_category(self):
        """Test that get_prs_for_user returns the new authored_changes_requested category"""
        # Mock the cache with a PR
        self.pr_cache.cache = {
            "test-repo": [
                {
                    "number": 123,
                    "title": "Test PR",
                    "html_url": "https://github.com/test-org/test-repo/pull/123",
                    "user": {"login": "test-author"},
                    "requested_reviewers": [{"login": "reviewer1"}],
                    "assignees": [],
                }
            ]
        }

        # Mock the cache as not expired by patching is_cache_expired
        with patch.object(self.pr_cache, "is_cache_expired") as mock_expired:
            mock_expired.return_value = False

            # Mock the review status check to return changes requested
            with patch.object(
                self.pr_cache, "_get_pr_review_status"
            ) as mock_review_status:
                mock_review_status.return_value = {
                    "has_changes_requested": True,
                    "has_approvals": False,
                }

                result = self.pr_cache.get_prs_for_user("test-author")

                # Verify that the new category exists and contains the PR
                self.assertIn("authored_changes_requested", result)
                self.assertEqual(len(result["authored_changes_requested"]), 1)
                self.assertEqual(result["authored_changes_requested"][0]["number"], 123)

                # Verify other categories are empty
                self.assertEqual(len(result["authored_approved"]), 0)
                self.assertEqual(len(result["assigned"]), 0)
                self.assertEqual(len(result["authored_unassigned"]), 0)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_prs_for_user_handles_review_status_error(self, mock_get):
        """Test that get_prs_for_user handles review status errors gracefully"""
        # Set up cache with a PR
        self.pr_cache.cache = {
            "test-repo": [
                {
                    "number": 123,
                    "title": "Test PR",
                    "draft": False,
                    "user": {"login": "test-author"},
                    "requested_reviewers": [{"login": "reviewer1"}],
                    "requested_teams": [],
                    "assignees": []
                }
            ]
        }
        self.pr_cache.last_updated = datetime.now()

        # Mock the review status to return None (error case)
        with patch.object(self.pr_cache, "_get_pr_review_status", return_value=None):
            result = self.pr_cache.get_prs_for_user("test-author")

            # PR should be in unknown status category when there's an error fetching review status
            self.assertIn("authored_unknown_status", result)
            self.assertEqual(len(result["authored_unknown_status"]), 1)
            self.assertEqual(result["authored_unknown_status"][0]["number"], 123)

            # Other categories should be empty
            self.assertEqual(len(result["authored_changes_requested"]), 0)
            self.assertEqual(len(result["authored_approved"]), 0)
            self.assertEqual(len(result["authored_pending_review"]), 0)


if __name__ == "__main__":
    unittest.main()