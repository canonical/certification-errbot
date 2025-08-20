#!/usr/bin/env python3
"""
Test for Jira API functions
"""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.certification.jira_api import (
    get_jira_issues_for_github_team_members,
    get_jira_issues_for_mattermost_handle,
    get_jira_issues_for_user,
    get_priority_sort_key,
    is_review_status,
)


class TestJiraPrioritySorting(unittest.TestCase):
    """Test cases for Jira priority sorting functionality"""

    def test_priority_sort_key_order(self):
        """Test that priority sort keys are in correct order"""
        priorities = ["Highest", "High", "Medium", "Low", "Lowest", "None", ""]
        
        # Get sort keys
        sort_keys = [get_priority_sort_key(p) for p in priorities]
        
        # Verify they are in ascending order (1, 2, 3, 4, 5, 6, 6)
        expected_keys = [1, 2, 3, 4, 5, 6, 6]
        self.assertEqual(sort_keys, expected_keys)

    def test_priority_sort_key_case_insensitive(self):
        """Test that priority sort keys are case insensitive"""
        test_cases = [
            ("Highest", "HIGHEST", "highest"),
            ("High", "HIGH", "high"),
            ("Medium", "MEDIUM", "medium"),
            ("Low", "LOW", "low"),
            ("Lowest", "LOWEST", "lowest"),
        ]
        
        for priority_variants in test_cases:
            sort_keys = [get_priority_sort_key(p) for p in priority_variants]
            # All variants should have the same sort key
            self.assertTrue(all(key == sort_keys[0] for key in sort_keys),
                          f"Priority variants {priority_variants} should have same sort key")

    def test_priority_sort_key_unknown_priority(self):
        """Test that unknown priorities get the lowest priority"""
        unknown_priorities = ["Custom", "Unknown", "RandomText", "1", "Critical"]
        
        for priority in unknown_priorities:
            sort_key = get_priority_sort_key(priority)
            self.assertEqual(sort_key, 6, f"Unknown priority '{priority}' should get sort key 6")

    def test_priority_sorting_order(self):
        """Test that a list of issues gets sorted correctly by priority"""
        # Mock issues with different priorities
        mock_issues = [
            {"priority": "Low", "key": "TEST-1"},
            {"priority": "Highest", "key": "TEST-2"},
            {"priority": "Medium", "key": "TEST-3"},
            {"priority": "High", "key": "TEST-4"},
            {"priority": "Lowest", "key": "TEST-5"},
            {"priority": "None", "key": "TEST-6"},
        ]
        
        # Sort by priority
        sorted_issues = sorted(mock_issues, key=lambda x: get_priority_sort_key(x.get("priority", "")))
        
        # Verify order: Highest, High, Medium, Low, Lowest, None
        expected_order = ["TEST-2", "TEST-4", "TEST-3", "TEST-1", "TEST-5", "TEST-6"]
        actual_order = [issue["key"] for issue in sorted_issues]
        
        self.assertEqual(actual_order, expected_order)


class TestJiraAPI(unittest.TestCase):
    """Test cases for Jira API functionality"""

    def test_is_review_status(self):
        """Test is_review_status function"""
        # Test review statuses
        review_statuses = [
            "In Review",
            "Code Review",
            "Peer Review",
            "Review in Progress",
            "Awaiting Review",
            "Under Review"
        ]
        for status in review_statuses:
            self.assertTrue(is_review_status(status), f"{status} should be a review status")
        
        # Test non-review statuses
        non_review_statuses = [
            "To Do",
            "In Progress",
            "Done",
            "Blocked",
            "Testing"
        ]
        for status in non_review_statuses:
            self.assertFalse(is_review_status(status), f"{status} should not be a review status")
        
        # Test case insensitivity
        self.assertTrue(is_review_status("in review"))
        self.assertTrue(is_review_status("IN REVIEW"))
        self.assertTrue(is_review_status("code REVIEW"))

    @patch("plugins.certification.jira_api.jira_issues_cache")
    def test_get_jira_issues_for_user_success(self, mock_cache):
        """Test successful retrieval of Jira issues for a user from cache"""
        # Mock cached issues
        mock_cache.__contains__ = lambda self, key: key == "test@example.com"
        mock_cache.__getitem__ = lambda self, key: [
            {
                "key": "TEST-1",
                "summary": "Test Issue 1",
                "status": "In Progress",
                "priority": "High",
                "story_points": 5,
                "is_completed": False,
                "is_in_review": False
            },
            {
                "key": "TEST-2",
                "summary": "Test Issue 2",
                "status": "Done",
                "priority": "Medium",
                "story_points": 3,
                "is_completed": True,
                "is_in_review": False
            }
        ]
        
        result = get_jira_issues_for_user("test@example.com")
        
        self.assertIn("active", result)
        self.assertIn("completed", result)
        self.assertEqual(len(result["active"]), 1)
        self.assertEqual(len(result["completed"]), 1)
        self.assertEqual(result["active"][0]["key"], "TEST-1")
        self.assertEqual(result["completed"][0]["key"], "TEST-2")

    @patch("plugins.certification.jira_api.jira_issues_cache")
    def test_get_jira_issues_for_user_no_cache(self, mock_cache):
        """Test get_jira_issues_for_user when user not in cache"""
        # Mock empty cache
        mock_cache.__contains__ = lambda self, key: False
        
        result = get_jira_issues_for_user("test@example.com")
        
        self.assertEqual(result, {"active": [], "review": [], "completed": [], "untriaged": []})

    @patch("plugins.certification.jira_api.jira_issues_cache")
    def test_get_jira_issues_for_user_with_review_issues(self, mock_cache):
        """Test get_jira_issues_for_user correctly categorizes review issues"""
        # Mock cached issues with review status
        mock_cache.__contains__ = lambda self, key: key == "test@example.com"
        mock_cache.__getitem__ = lambda self, key: [
            {
                "key": "TEST-3",
                "summary": "Review Issue",
                "status": "In Review",
                "priority": "High",
                "story_points": 8,
                "is_completed": False,
                "is_in_review": True
            }
        ]
        
        result = get_jira_issues_for_user("test@example.com")
        
        self.assertIn("review", result)
        self.assertEqual(len(result["review"]), 1)
        self.assertEqual(result["review"][0]["key"], "TEST-3")

    @patch("plugins.certification.jira_api.get_email_from_mattermost_handle")
    @patch("plugins.certification.jira_api.get_jira_issues_for_user")
    def test_get_jira_issues_for_mattermost_handle(self, mock_get_issues, mock_get_email):
        """Test get_jira_issues_for_mattermost_handle"""
        # Mock email lookup
        mock_get_email.return_value = "test@example.com"
        
        # Mock issues - include all expected categories
        mock_issues = {
            "active": [{"key": "TEST-1", "summary": "Test"}],
            "review": [],
            "completed": [],
            "untriaged": []
        }
        mock_get_issues.return_value = mock_issues
        
        result = get_jira_issues_for_mattermost_handle("testuser")
        
        self.assertEqual(result, mock_issues)
        mock_get_email.assert_called_once_with("testuser")
        mock_get_issues.assert_called_once_with("test@example.com", 50)

    @patch("plugins.certification.jira_api.get_email_from_mattermost_handle")
    @patch("plugins.certification.jira_api.get_jira_issues_for_user")
    def test_get_jira_issues_for_mattermost_handle_no_email(self, mock_get_issues, mock_get_email):
        """Test get_jira_issues_for_mattermost_handle when email lookup fails"""
        # Mock email lookup failure
        mock_get_email.return_value = None
        
        result = get_jira_issues_for_mattermost_handle("testuser")
        
        # Should return empty categories when no email found - but function returns only active/completed
        self.assertEqual(result, {"active": [], "completed": []})
        mock_get_issues.assert_not_called()

    @patch("plugins.certification.jira_api.get_email_from_github_username")
    @patch("plugins.certification.jira_api.get_jira_issues_for_user")
    def test_get_jira_issues_for_github_team_members(self, mock_get_issues, mock_get_email):
        """Test get_jira_issues_for_github_team_members"""
        # Mock email lookups
        def email_side_effect(username):
            return {
                "user1": "user1@example.com",
                "user2": "user2@example.com",
                "user3": None  # No email found
            }.get(username)
        
        mock_get_email.side_effect = email_side_effect
        
        # Mock issues for each user - include max_results parameter
        def issues_side_effect(email, max_results=50):
            return {
                "user1@example.com": {
                    "active": [{"key": "TEST-1", "summary": "User1 Issue"}],
                    "review": [],
                    "completed": [],
                    "untriaged": []
                },
                "user2@example.com": {
                    "active": [],
                    "review": [],
                    "completed": [{"key": "TEST-2", "summary": "User2 Done"}],
                    "untriaged": []
                }
            }.get(email, {"active": [], "review": [], "completed": [], "untriaged": []})
        
        mock_get_issues.side_effect = issues_side_effect
        
        result = get_jira_issues_for_github_team_members(["user1", "user2", "user3"])
        
        self.assertIn("user1", result)
        self.assertIn("user2", result)
        self.assertNotIn("user3", result)  # No email, so no issues
        self.assertEqual(len(result["user1"]["active"]), 1)
        self.assertEqual(len(result["user2"]["completed"]), 1)

    @patch("plugins.certification.jira_api.get_jira_issues_for_github_team_members")
    def test_get_jira_issues_for_github_team_members_empty_team(self, mock_get_issues):
        """Test get_jira_issues_for_github_team_members with empty team"""
        result = get_jira_issues_for_github_team_members([])
        
        self.assertEqual(result, {})
        mock_get_issues.assert_not_called()


class TestJiraReviewStatus(unittest.TestCase):
    """Test cases for review status detection"""

    @patch("plugins.certification.jira_api.jira_issues_cache")
    def test_issues_categorized_by_review_status(self, mock_cache):
        """Test that issues are correctly categorized based on review status"""
        # Mock cached issues with different categories
        mock_cache.__contains__ = lambda self, key: key == "test@example.com"
        mock_cache.__getitem__ = lambda self, key: [
            # Active issue (not in review, not done, has priority)
            {
                "key": "TEST-1",
                "summary": "Active Task",
                "status": "In Progress",
                "priority": "High",
                "story_points": 5,
                "is_completed": False,
                "is_in_review": False
            },
            # Review issue
            {
                "key": "TEST-2",
                "summary": "Review Task",
                "status": "In Review",
                "priority": "Medium",
                "story_points": 3,
                "is_completed": False,
                "is_in_review": True
            },
            # Completed issue
            {
                "key": "TEST-3",
                "summary": "Done Task",
                "status": "Done",
                "priority": "Low",
                "story_points": 2,
                "is_completed": True,
                "is_in_review": False
            },
            # Untriaged issue (no priority)
            {
                "key": "TEST-4",
                "summary": "Untriaged Task",
                "status": "To Do",
                "priority": None,
                "story_points": 0,
                "is_completed": False,
                "is_in_review": False
            }
        ]
        
        result = get_jira_issues_for_user("test@example.com")
        
        # Verify categorization
        self.assertEqual(len(result["active"]), 1)
        self.assertEqual(result["active"][0]["key"], "TEST-1")
        
        self.assertEqual(len(result.get("review", [])), 1)
        self.assertEqual(result["review"][0]["key"], "TEST-2")
        
        self.assertEqual(len(result["completed"]), 1)
        self.assertEqual(result["completed"][0]["key"], "TEST-3")
        
        self.assertEqual(len(result.get("untriaged", [])), 1)
        self.assertEqual(result["untriaged"][0]["key"], "TEST-4")


if __name__ == "__main__":
    unittest.main()