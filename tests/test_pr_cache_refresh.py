#!/usr/bin/env python3
"""
Test for the PullRequestCache refresh_cache method with mocked GitHub connectivity
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

from plugins.certification.pr_cache import PullRequestCache


class TestPRCacheRefresh(unittest.TestCase):
    """Test cases for PR cache refresh functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.pr_cache = PullRequestCache(
            repo_filter=["repo1", "repo2"],
            github_token="test-token",
            github_org="test-org"
        )

    @patch("plugins.certification.pr_cache.requests.get")
    def test_refresh_cache_success_with_filter(self, mock_get):
        """Test successful cache refresh with repository filter"""
        # Mock responses for two repositories
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            page = kwargs.get("params", {}).get("page", 1)
            
            if "repo1/pulls" in url:
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {
                            "number": 1,
                            "title": "PR 1",
                            "draft": False,
                            "user": {"login": "author1"},
                            "requested_reviewers": [],
                            "assignees": []
                        },
                        {
                            "number": 2,
                            "title": "PR 2",
                            "draft": True,  # This should be filtered out
                            "user": {"login": "author2"},
                            "requested_reviewers": [],
                            "assignees": []
                        }
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            elif "repo2/pulls" in url:
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {
                            "number": 3,
                            "title": "PR 3",
                            "draft": False,
                            "user": {"login": "author3"},
                            "requested_reviewers": [],
                            "assignees": []
                        }
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = []
            
            return mock_response

        mock_get.side_effect = side_effect

        # Execute refresh_cache
        result = self.pr_cache.refresh_cache()

        # Assertions
        self.assertTrue(result)
        self.assertEqual(len(self.pr_cache.cache), 2)
        self.assertEqual(len(self.pr_cache.cache["repo1"]), 1)  # Draft PR filtered out
        self.assertEqual(len(self.pr_cache.cache["repo2"]), 1)
        self.assertIsNotNone(self.pr_cache.last_updated)
        self.assertIsInstance(self.pr_cache.last_updated, datetime)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_refresh_cache_handles_404_repos(self, mock_get):
        """Test that refresh_cache handles 404 errors for non-existent repos"""
        # Mock responses - one successful, one 404
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            page = kwargs.get("params", {}).get("page", 1)
            
            if "repo1/pulls" in url:
                mock_response.status_code = 404
                mock_response.json.return_value = {"message": "Not Found"}
            elif "repo2/pulls" in url:
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {
                            "number": 1,
                            "title": "PR 1",
                            "draft": False,
                            "user": {"login": "author1"},
                            "requested_reviewers": [],
                            "assignees": []
                        }
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = []
            
            return mock_response

        mock_get.side_effect = side_effect

        # Execute refresh_cache
        result = self.pr_cache.refresh_cache()

        # Assertions
        self.assertTrue(result)
        self.assertEqual(len(self.pr_cache.cache), 2)
        self.assertEqual(len(self.pr_cache.cache["repo1"]), 0)  # 404 returns empty list
        self.assertEqual(len(self.pr_cache.cache["repo2"]), 1)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_refresh_cache_without_filter_fetches_org_repos(self, mock_get):
        """Test that refresh_cache fetches all org repos when no filter is provided"""
        # Create cache without filter
        pr_cache = PullRequestCache(
            github_token="test-token",
            github_org="test-org"
        )

        # Mock responses
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            
            if "/orgs/test-org/repos" in url:
                # Return org repos based on page
                page = kwargs.get("params", {}).get("page", 1)
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {"name": "org-repo1"},
                        {"name": "org-repo2"}
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            elif "org-repo1/pulls" in url:
                page = kwargs.get("params", {}).get("page", 1)
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {
                            "number": 1,
                            "title": "PR 1",
                            "draft": False,
                            "user": {"login": "author1"},
                            "requested_reviewers": [],
                            "assignees": []
                        }
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            elif "org-repo2/pulls" in url:
                page = kwargs.get("params", {}).get("page", 1)
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = []
            
            return mock_response

        mock_get.side_effect = side_effect

        # Execute refresh_cache
        result = pr_cache.refresh_cache()

        # Assertions
        self.assertTrue(result)
        self.assertEqual(len(pr_cache.cache), 2)
        self.assertIn("org-repo1", pr_cache.cache)
        self.assertIn("org-repo2", pr_cache.cache)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_refresh_cache_handles_request_exceptions(self, mock_get):
        """Test that refresh_cache handles network errors gracefully"""
        import requests
        
        # Mock network error for first repo, success for second
        def side_effect(url, **kwargs):
            page = kwargs.get("params", {}).get("page", 1)
            
            if "repo1/pulls" in url:
                raise requests.exceptions.RequestException("Network error")
            elif "repo2/pulls" in url:
                if page == 1:
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {
                            "number": 1,
                            "title": "PR 1",
                            "draft": False,
                            "user": {"login": "author1"},
                            "requested_reviewers": [],
                            "assignees": []
                        }
                    ]
                    return mock_response
                else:
                    mock_response = MagicMock()
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
                    return mock_response
            else:
                mock_response = MagicMock()
                mock_response.status_code = 200
                mock_response.json.return_value = []
                return mock_response

        mock_get.side_effect = side_effect

        # Execute refresh_cache
        result = self.pr_cache.refresh_cache()

        # Assertions - should still succeed but only have data for repo2
        self.assertTrue(result)
        self.assertEqual(len(self.pr_cache.cache), 1)
        self.assertIn("repo2", self.pr_cache.cache)
        self.assertNotIn("repo1", self.pr_cache.cache)

    @patch("plugins.certification.pr_cache.requests.get")
    def test_refresh_cache_pagination(self, mock_get):
        """Test that refresh_cache handles pagination correctly"""
        # Mock responses with pagination
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            page = kwargs.get("params", {}).get("page", 1)
            
            if "repo1/pulls" in url:
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {
                            "number": i,
                            "title": f"PR {i}",
                            "draft": False,
                            "user": {"login": f"author{i}"},
                            "requested_reviewers": [],
                            "assignees": []
                        }
                        for i in range(1, 101)  # 100 PRs (full page)
                    ]
                elif page == 2:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {
                            "number": i,
                            "title": f"PR {i}",
                            "draft": False,
                            "user": {"login": f"author{i}"},
                            "requested_reviewers": [],
                            "assignees": []
                        }
                        for i in range(101, 111)  # 10 more PRs
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = []
            
            return mock_response

        mock_get.side_effect = side_effect

        # Create cache with only repo1 for simplicity
        pr_cache = PullRequestCache(
            repo_filter=["repo1"],
            github_token="test-token",
            github_org="test-org"
        )

        # Execute refresh_cache
        result = pr_cache.refresh_cache()

        # Assertions
        self.assertTrue(result)
        self.assertEqual(len(pr_cache.cache["repo1"]), 110)  # Total PRs from both pages

    @patch("plugins.certification.pr_cache.requests.get")
    def test_refresh_cache_filters_draft_prs(self, mock_get):
        """Test that refresh_cache filters out draft PRs"""
        # Mock response with mix of draft and non-draft PRs
        def side_effect(url, **kwargs):
            mock_response = MagicMock()
            page = kwargs.get("params", {}).get("page", 1)
            
            if "test-repo/pulls" in url:
                if page == 1:
                    mock_response.status_code = 200
                    mock_response.json.return_value = [
                        {
                            "number": 1,
                            "title": "Regular PR",
                            "draft": False,
                            "user": {"login": "author1"},
                            "requested_reviewers": [],
                            "assignees": []
                        },
                        {
                            "number": 2,
                            "title": "Draft PR",
                            "draft": True,
                            "user": {"login": "author2"},
                            "requested_reviewers": [],
                            "assignees": []
                        },
                        {
                            "number": 3,
                            "title": "Another Regular PR",
                            "draft": False,
                            "user": {"login": "author3"},
                            "requested_reviewers": [],
                            "assignees": []
                        }
                    ]
                else:
                    mock_response.status_code = 200
                    mock_response.json.return_value = []
            else:
                mock_response.status_code = 200
                mock_response.json.return_value = []
            
            return mock_response
        
        mock_get.side_effect = side_effect

        # Create cache with single repo
        pr_cache = PullRequestCache(
            repo_filter=["test-repo"],
            github_token="test-token",
            github_org="test-org"
        )

        # Execute refresh_cache
        result = pr_cache.refresh_cache()

        # Assertions
        self.assertTrue(result)
        self.assertEqual(len(pr_cache.cache["test-repo"]), 2)  # Only non-draft PRs
        pr_numbers = [pr["number"] for pr in pr_cache.cache["test-repo"]]
        self.assertIn(1, pr_numbers)
        self.assertIn(3, pr_numbers)
        self.assertNotIn(2, pr_numbers)  # Draft PR should be filtered out

    @patch("plugins.certification.pr_cache.requests.get")
    def test_refresh_cache_exception_returns_false(self, mock_get):
        """Test that refresh_cache returns False when exception occurs"""
        # Mock exception during fetch
        mock_get.side_effect = Exception("Critical error")

        # Execute refresh_cache
        result = self.pr_cache.refresh_cache()

        # Assertions
        self.assertFalse(result)

    def test_is_cache_expired_when_never_updated(self):
        """Test that cache is expired when never updated"""
        self.assertTrue(self.pr_cache.is_cache_expired())

    def test_is_cache_expired_after_update(self):
        """Test that cache is not expired immediately after update"""
        self.pr_cache.last_updated = datetime.now()
        self.assertFalse(self.pr_cache.is_cache_expired())

    @patch("plugins.certification.pr_cache.datetime")
    def test_is_cache_expired_after_timeout(self, mock_datetime):
        """Test that cache expires after timeout period"""
        from datetime import timedelta
        
        # Set last_updated to now
        now = datetime.now()
        self.pr_cache.last_updated = now
        
        # Mock datetime.now() to return time after expiry
        mock_datetime.now.return_value = now + timedelta(minutes=16)
        
        self.assertTrue(self.pr_cache.is_cache_expired())


if __name__ == "__main__":
    unittest.main()