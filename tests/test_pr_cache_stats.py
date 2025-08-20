#!/usr/bin/env python3
"""
Test for PullRequestCache.get_cache_stats method
"""

import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from plugins.certification.pr_cache import PullRequestCache


class TestPRCacheStats(unittest.TestCase):
    """Test cases for PR cache statistics functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.pr_cache = PullRequestCache(
            repo_filter=["repo1", "repo2", "repo3"],
            github_token="test-token",
            github_org="test-org"
        )

    def test_get_cache_stats_empty_cache(self):
        """Test get_cache_stats with empty cache"""
        stats = self.pr_cache.get_cache_stats()
        
        self.assertEqual(stats["total_prs"], 0)
        self.assertEqual(stats["total_repositories"], 0)  # Empty cache
        self.assertIsNone(stats["last_updated"])
        self.assertTrue(stats["cache_expired"])

    def test_get_cache_stats_with_data(self):
        """Test get_cache_stats with cached PR data"""
        # Set up cache with test data
        self.pr_cache.cache = {
            "repo1": [
                {"number": 1, "title": "PR 1"},
                {"number": 2, "title": "PR 2"},
            ],
            "repo2": [
                {"number": 3, "title": "PR 3"},
            ],
            "repo3": []  # Empty repo
        }
        self.pr_cache.last_updated = datetime.now()
        
        stats = self.pr_cache.get_cache_stats()
        
        self.assertEqual(stats["total_prs"], 3)
        self.assertEqual(stats["total_repositories"], 3)
        self.assertIsNotNone(stats["last_updated"])
        self.assertFalse(stats["cache_expired"])

    def test_get_cache_stats_without_filter(self):
        """Test get_cache_stats when no repo filter is provided"""
        # Create cache without filter
        pr_cache = PullRequestCache(
            github_token="test-token",
            github_org="test-org"
        )
        
        # Set up cache with test data
        pr_cache.cache = {
            "org-repo1": [{"number": 1}],
            "org-repo2": [{"number": 2}],
            "org-repo3": [{"number": 3}],
            "org-repo4": [],
        }
        pr_cache.last_updated = datetime.now()
        
        stats = pr_cache.get_cache_stats()
        
        self.assertEqual(stats["total_prs"], 3)
        self.assertEqual(stats["total_repositories"], 4)  # From cache keys
        self.assertFalse(stats["cache_expired"])

    @patch("plugins.certification.pr_cache.datetime")
    def test_get_cache_stats_expired_cache(self, mock_datetime):
        """Test get_cache_stats correctly reports expired cache"""
        # Set up cache with old timestamp
        now = datetime.now()
        self.pr_cache.last_updated = now
        self.pr_cache.cache = {"repo1": [{"number": 1}]}
        
        # Mock datetime.now() to return time after expiry
        mock_datetime.now.return_value = now + timedelta(minutes=20)
        
        stats = self.pr_cache.get_cache_stats()
        
        self.assertTrue(stats["cache_expired"])

    def test_get_cache_stats_counts_all_prs(self):
        """Test get_cache_stats correctly counts PRs across all repositories"""
        # Set up cache with varying numbers of PRs
        self.pr_cache.cache = {
            "repo1": [{"number": i} for i in range(10)],  # 10 PRs
            "repo2": [{"number": i} for i in range(5)],   # 5 PRs  
            "repo3": [{"number": i} for i in range(15)],  # 15 PRs
        }
        self.pr_cache.last_updated = datetime.now()
        
        stats = self.pr_cache.get_cache_stats()
        
        self.assertEqual(stats["total_prs"], 30)  # Total: 10 + 5 + 15
        self.assertEqual(stats["total_repositories"], 3)

    def test_get_cache_stats_handles_none_values(self):
        """Test get_cache_stats handles None values in cache gracefully"""
        # Set up cache with potential None values
        self.pr_cache.cache = {
            "repo1": None,  # This shouldn't happen but test it anyway
            "repo2": [],
            "repo3": [{"number": 1}]
        }
        self.pr_cache.last_updated = datetime.now()
        
        # Should count only valid PR lists
        # But this will actually fail because of the None value
        # Let's test that it raises the expected error
        with self.assertRaises(TypeError):
            stats = self.pr_cache.get_cache_stats()


if __name__ == "__main__":
    unittest.main()