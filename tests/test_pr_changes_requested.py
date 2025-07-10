#!/usr/bin/env python3
"""
Test for the new "changes requested" PR functionality
"""

import unittest
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
    def test_get_pr_review_status_with_changes_requested(self, mock_get):
        """Test that _get_pr_review_status correctly identifies changes requested"""
        # Mock response with changes requested review
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"state": "COMMENTED", "user": {"login": "reviewer1"}},
            {"state": "CHANGES_REQUESTED", "user": {"login": "reviewer2"}},
        ]
        mock_get.return_value = mock_response

        result = self.pr_cache._get_pr_review_status("test-repo", 123)

        self.assertTrue(result["has_changes_requested"])
        self.assertFalse(result["has_approvals"])

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_pr_review_status_with_approvals(self, mock_get):
        """Test that _get_pr_review_status correctly identifies approvals"""
        # Mock response with approved review
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"state": "COMMENTED", "user": {"login": "reviewer1"}},
            {"state": "APPROVED", "user": {"login": "reviewer2"}},
        ]
        mock_get.return_value = mock_response

        result = self.pr_cache._get_pr_review_status("test-repo", 123)

        self.assertFalse(result["has_changes_requested"])
        self.assertTrue(result["has_approvals"])

    @patch("plugins.certification.pr_cache.requests.get")
    def test_get_pr_review_status_with_both(self, mock_get):
        """Test that _get_pr_review_status handles both approvals and changes requested"""
        # Mock response with both approved and changes requested reviews
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"state": "APPROVED", "user": {"login": "reviewer1"}},
            {"state": "CHANGES_REQUESTED", "user": {"login": "reviewer2"}},
        ]
        mock_get.return_value = mock_response

        result = self.pr_cache._get_pr_review_status("test-repo", 123)

        self.assertTrue(result["has_changes_requested"])
        self.assertTrue(result["has_approvals"])

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


if __name__ == "__main__":
    unittest.main()
