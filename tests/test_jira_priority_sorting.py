#!/usr/bin/env python3
"""
Test for Jira priority sorting functionality
"""
import unittest
from plugins.certification.jira_api import get_priority_sort_key


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


if __name__ == '__main__':
    unittest.main()