"""Test Jira formatter handles None story points correctly."""

import unittest

from plugins.certification.formatting.jira_formatter import (
    format_jira_summary,
    format_story_points,
    format_team_jira_summary,
)


class TestJiraFormatterNoneHandling(unittest.TestCase):
    """Test that the Jira formatter properly handles None story points."""

    def test_format_story_points_with_none(self):
        """Test format_story_points handles None values."""
        self.assertEqual(format_story_points(None), "")
        self.assertEqual(format_story_points(0), "")
        self.assertEqual(format_story_points(1), " (1 story point)")
        self.assertEqual(format_story_points(5), " (5 story points)")

    def test_format_jira_summary_with_none_story_points(self):
        """Test that None story points don't cause arithmetic errors."""
        jira_data = {
            "active": [
                {
                    "key": "CERT-1",
                    "url": "http://jira.example.com/CERT-1",
                    "summary": "Issue with None points",
                    "story_points": None,
                },
                {
                    "key": "CERT-2",
                    "url": "http://jira.example.com/CERT-2",
                    "summary": "Issue with 3 points",
                    "story_points": 3,
                },
            ],
            "review": [
                {
                    "key": "CERT-3",
                    "url": "http://jira.example.com/CERT-3",
                    "summary": "Issue missing story_points key",
                    # No story_points key at all
                },
                {
                    "key": "CERT-4",
                    "url": "http://jira.example.com/CERT-4",
                    "summary": "Issue with 5 points",
                    "story_points": 5,
                },
            ],
            "completed": [
                {
                    "key": "CERT-5",
                    "url": "http://jira.example.com/CERT-5",
                    "summary": "Issue with 0 points",
                    "story_points": 0,
                },
                {
                    "key": "CERT-6",
                    "url": "http://jira.example.com/CERT-6",
                    "summary": "Issue with 2 points",
                    "story_points": 2,
                },
            ],
        }

        # This should not raise a TypeError
        result = format_jira_summary("testuser", jira_data, show_completed=True)

        # Verify the output contains expected sections
        self.assertIn("## Jira Issues", result)
        self.assertIn("Active (3 story points)", result)
        self.assertIn("In Review (5 story points)", result)
        self.assertIn("Completed during the pulse (2 story points)", result)
        self.assertIn("Total (10 story points)", result)

        # Verify all issues are present
        self.assertIn("CERT-1", result)
        self.assertIn("CERT-2", result)
        self.assertIn("CERT-3", result)
        self.assertIn("CERT-4", result)
        self.assertIn("CERT-5", result)
        self.assertIn("CERT-6", result)

    def test_format_jira_summary_with_all_none_points(self):
        """Test when all issues have None story points."""
        jira_data = {
            "active": [
                {
                    "key": "CERT-7",
                    "url": "http://jira.example.com/CERT-7",
                    "summary": "Issue with None",
                    "story_points": None,
                },
            ],
            "review": [
                {
                    "key": "CERT-8",
                    "url": "http://jira.example.com/CERT-8",
                    "summary": "Another None issue",
                    "story_points": None,
                },
            ],
        }

        result = format_jira_summary("testuser", jira_data, show_completed=False)

        # Should not have story points displayed when all are None/0
        self.assertIn("**Active:**", result)
        self.assertIn("**In Review:**", result)
        self.assertNotIn("story point", result)
        self.assertNotIn("**Total", result)  # No total when points are 0

    def test_format_jira_summary_with_empty_categories(self):
        """Test with some empty issue categories."""
        jira_data = {
            "active": [],
            "review": [
                {
                    "key": "CERT-9",
                    "url": "http://jira.example.com/CERT-9",
                    "summary": "Single review issue",
                    "story_points": 8,
                },
            ],
            "completed": [],
        }

        result = format_jira_summary("testuser", jira_data, show_completed=True)

        self.assertIn("In Review (8 story points)", result)
        self.assertIn("Total (8 story points)", result)
        self.assertNotIn("**Active", result)
        self.assertNotIn("**Completed", result)

    def test_format_jira_summary_mixed_none_and_valid_points(self):
        """Test calculation with mix of None, 0, and valid story points."""
        jira_data = {
            "active": [
                {"key": "A1", "url": "http://j.com/A1", "summary": "None", "story_points": None},
                {"key": "A2", "url": "http://j.com/A2", "summary": "Zero", "story_points": 0},
                {"key": "A3", "url": "http://j.com/A3", "summary": "Five", "story_points": 5},
            ],
            "review": [
                {"key": "R1", "url": "http://j.com/R1", "summary": "Missing"},  # No story_points key
                {"key": "R2", "url": "http://j.com/R2", "summary": "Three", "story_points": 3},
            ],
            "completed": [
                {"key": "C1", "url": "http://j.com/C1", "summary": "None", "story_points": None},
                {"key": "C2", "url": "http://j.com/C2", "summary": "Seven", "story_points": 7},
            ],
        }

        result = format_jira_summary("user", jira_data, show_completed=True)

        # Total should be 5 + 3 + 7 = 15 (None and 0 values don't contribute)
        self.assertIn("Total (15 story points)", result)
        self.assertIn("Active (5 story points)", result)
        self.assertIn("In Review (3 story points)", result)
        self.assertIn("Completed during the pulse (7 story points)", result)

    def test_format_team_jira_summary_with_none_points(self):
        """Test team summary handles None story points."""
        team_data = {
            "alice": {
                "active": [
                    {
                        "key": "ALICE-1",
                        "url": "http://j.com/ALICE-1",
                        "summary": "Alice task",
                        "story_points": None,
                    },
                ],
                "review": [],
            },
            "bob": {
                "active": [
                    {
                        "key": "BOB-1",
                        "url": "http://j.com/BOB-1",
                        "summary": "Bob task",
                        "story_points": 5,
                    },
                ],
                "review": [],
            },
        }

        user_handles = {"alice": "alice_mm", "bob": "bob_mm"}

        # Should not raise an error
        result = format_team_jira_summary("test-team", team_data, user_handles)

        self.assertIn("test-team", result)
        self.assertIn("ALICE-1", result)
        self.assertIn("BOB-1", result)
        # Bob's section should show points, Alice's should not
        self.assertIn("Active (5 story points)", result)

    def test_edge_case_negative_story_points(self):
        """Test handling of unexpected negative story points."""
        jira_data = {
            "active": [
                {
                    "key": "NEG-1",
                    "url": "http://j.com/NEG-1",
                    "summary": "Negative points",
                    "story_points": -5,
                },
                {
                    "key": "POS-1",
                    "url": "http://j.com/POS-1",
                    "summary": "Positive points",
                    "story_points": 10,
                },
            ],
            "review": [],
        }

        result = format_jira_summary("user", jira_data)

        # Should handle negative values (sum would be 5)
        self.assertIn("Active (5 story points)", result)
        self.assertIn("Total (5 story points)", result)

    def test_edge_case_float_story_points(self):
        """Test handling of float story points (e.g., 0.5, 1.5)."""
        jira_data = {
            "active": [
                {
                    "key": "FLOAT-1",
                    "url": "http://j.com/FLOAT-1",
                    "summary": "Half point",
                    "story_points": 0.5,
                },
                {
                    "key": "FLOAT-2",
                    "url": "http://j.com/FLOAT-2",
                    "summary": "One and half",
                    "story_points": 1.5,
                },
            ],
            "review": [],
        }

        result = format_jira_summary("user", jira_data)

        # Should handle float values (sum would be 2.0)
        self.assertIn("Active (2", result)  # Could be 2 or 2.0
        self.assertIn("Total (2", result)


if __name__ == "__main__":
    unittest.main()