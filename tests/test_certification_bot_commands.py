#!/usr/bin/env python3
"""
Test for certification bot commands
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, Mock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from plugins.certification.certification import CertificationPlugin


class TestCertificationBotCommands(unittest.TestCase):
    """Test cases for certification bot commands"""

    def setUp(self):
        """Set up test fixtures"""
        bot = MagicMock()
        # Mock the PullRequestCache to prevent real API calls
        with patch('plugins.certification.certification.PullRequestCache'):
            self.plugin = CertificationPlugin(bot, "CertificationPlugin")
        # Mock the pr_cache methods
        self.plugin.pr_cache = MagicMock()
        self.msg = MagicMock()
        self.msg.frm.username = "testuser"

    @patch("plugins.certification.certification.reply_with_artefacts_summary")
    def test_artefacts_command(self, mock_reply):
        """Test !artefacts command"""
        mock_reply.return_value = "Test artefacts summary"
        
        result = self.plugin.artefacts(self.msg, ["filter1", "filter2"])
        
        self.assertEqual(result, "Test artefacts summary")
        mock_reply.assert_called_once_with(self.msg.frm, ["filter1", "filter2"])

    @patch("plugins.certification.certification.reply_with_artefacts_summary")
    def test_artefacts_command_error(self, mock_reply):
        """Test !artefacts command error handling"""
        mock_reply.side_effect = Exception("Test error")
        
        result = self.plugin.artefacts(self.msg, [])
        
        self.assertIn("Error processing artefacts command", result)

    @patch.object(CertificationPlugin, "_get_github_username_for_user")
    @patch.object(CertificationPlugin, "_format_pr_summary")
    def test_prs_command_with_cache(self, mock_format, mock_get_github):
        """Test !prs command with cached data"""
        mock_get_github.return_value = "github_user"
        mock_format.return_value = "PR summary"
        
        # Mock the PR cache
        self.plugin.pr_cache = MagicMock()
        self.plugin.pr_cache.get_prs_for_user.return_value = {
            "assigned": [],
            "authored_unassigned": [],
            "authored_approved": [],
            "authored_changes_requested": [],
            "authored_pending_review": [],
            "authored_unknown_status": []
        }
        
        result = self.plugin.prs(self.msg, [])
        
        self.assertEqual(result, "PR summary")
        self.plugin.pr_cache.get_prs_for_user.assert_called_once_with("github_user")

    @patch.object(CertificationPlugin, "_get_github_username_for_user")
    def test_prs_command_no_github_token(self, mock_get_github):
        """Test !prs command without GitHub token"""
        mock_get_github.return_value = "github_user"
        
        with patch("plugins.certification.certification.github_token", None):
            result = self.plugin.prs(self.msg, [])
        
        self.assertIn("GitHub token not configured", result)

    @patch("plugins.certification.certification.get_c3_token")
    @patch("plugins.certification.certification.get_physicalmachinesview")
    @patch("plugins.certification.certification.C3Client")
    def test_cid_command(self, mock_c3_client_class, mock_get_machines, mock_get_c3_token):
        """Test !cid command"""
        # Mock the C3 token
        mock_get_c3_token.return_value = "test-token"
        # Mock C3 client
        mock_c3_client = MagicMock()
        mock_c3_client_class.return_value = mock_c3_client
        mock_c3_client.__enter__ = Mock(return_value=mock_c3_client)
        mock_c3_client.__exit__ = Mock(return_value=None)
        
        # Mock machine response
        mock_machine = MagicMock()
        mock_machine.make = "Dell"
        mock_machine.model = "XPS"
        mock_machine.tf_provision_type = "Manual"
        
        mock_response = MagicMock()
        mock_response.parsed = [mock_machine]
        mock_response.make = "Dell"
        mock_response.model = "XPS"
        
        mock_get_machines.return_value = mock_response
        
        result = self.plugin.cid(self.msg, ["CID123"])
        
        self.assertIn("Dell", result)
        self.assertIn("XPS", result)
        self.assertIn("Manual", result)

    @patch("plugins.certification.certification.get_jira_issues_for_mattermost_handle")
    def test_jira_command_no_issues(self, mock_get_issues):
        """Test !jira command with no issues"""
        mock_get_issues.return_value = {
            "active": [],
            "review": [],
            "completed": [],
            "untriaged": []
        }
        
        result = self.plugin.jira(self.msg, [])
        
        self.assertEqual(result, "You have no Jira issues assigned")

    @patch("plugins.certification.certification.get_jira_issues_for_mattermost_handle")
    def test_jira_command_with_issues(self, mock_get_issues):
        """Test !jira command with issues"""
        mock_get_issues.return_value = {
            "active": [
                {
                    "key": "TEST-1",
                    "summary": "Active issue",
                    "status": "In Progress",
                    "priority": "High",
                    "story_points": 5,
                    "url": "http://jira/TEST-1"
                }
            ],
            "review": [],
            "completed": [
                {
                    "key": "TEST-2",
                    "summary": "Done issue",
                    "status": "Done",
                    "priority": "Low",
                    "story_points": 3,
                    "url": "http://jira/TEST-2"
                }
            ],
            "untriaged": []
        }
        
        # Mock the format story points method
        self.plugin._format_story_points = lambda x: f" ({x} SP)" if x else ""
        
        result = self.plugin.jira(self.msg, ["otheruser"])
        
        self.assertIn("Your assigned issues:", result)
        self.assertIn("Active (5 story points)", result)
        self.assertIn("TEST-1", result)
        self.assertIn("Completed during the pulse (3 story points)", result)
        self.assertIn("TEST-2", result)

    @patch("plugins.certification.certification.get_jira_issues_for_github_team_members")
    def test_team_jira_command_no_team(self, mock_get_issues):
        """Test !team_jira command without team configured"""
        with patch("plugins.certification.certification.github_team", None):
            result = self.plugin.team_jira(self.msg, [])
        
        self.assertIn("No GitHub team configured", result)

    @patch("plugins.certification.certification.get_mattermost_handle_from_github_username")
    @patch("plugins.certification.certification.get_jira_issues_for_github_team_members")
    def test_team_jira_command_with_issues(self, mock_get_issues, mock_get_handle):
        """Test !team_jira command with team issues"""
        # Mock team members
        self.plugin.pr_cache = MagicMock()
        self.plugin.pr_cache.get_team_members.return_value = ["user1", "user2"]
        
        # Mock issues
        mock_get_issues.return_value = {
            "user1": {
                "active": [
                    {
                        "key": "TEST-1",
                        "summary": "User1 issue",
                        "status": "In Progress",
                        "priority": "High",
                        "story_points": 5,
                        "url": "http://jira/TEST-1"
                    }
                ],
                "review": [],
                "completed": [],
                "untriaged": []
            }
        }
        
        # Mock Mattermost handle lookup
        mock_get_handle.return_value = "mm_user1"
        
        # Mock the format story points method
        self.plugin._format_story_points = lambda x: f" ({x} SP)" if x else ""
        
        with patch("plugins.certification.certification.github_team", "test-team"):
            result = self.plugin.team_jira(self.msg, [])
        
        self.assertIn("Jira issues assigned to team test-team", result)
        self.assertIn("@mm_user1", result)
        self.assertIn("TEST-1", result)

    @patch("plugins.certification.certification.get_llm_client")
    @patch("plugins.certification.certification.LLM_AVAILABLE", True)
    def test_sprint_summary_no_llm_client(self, mock_get_client):
        """Test !sprint_summary command without LLM client"""
        mock_get_client.return_value = None
        
        result = self.plugin.sprint_summary(self.msg, [])
        
        self.assertIn("LLM API not configured", result)

    @patch("plugins.certification.certification.get_llm_client")
    @patch("plugins.certification.certification.LLM_AVAILABLE", True)
    def test_sprint_summary_llm_unavailable(self, mock_get_client):
        """Test !sprint_summary command with LLM unavailable"""
        with patch("plugins.certification.certification.LLM_AVAILABLE", False):
            result = self.plugin.sprint_summary(self.msg, [])
        
        self.assertIn("LLM functionality not available", result)

    @patch('plugins.certification.certification.reply_with_artefacts_summary')
    @patch.object(CertificationPlugin, '_get_github_username_for_user')
    @patch.object(CertificationPlugin, '_generate_user_digest')
    def test_digest_command(self, mock_generate_digest, mock_get_github, mock_artefacts):
        """Test !digest command"""
        # Mock the GitHub username lookup
        mock_get_github.return_value = "github_user"
        # Mock the digest generation
        mock_generate_digest.return_value = "Test digest content"
        # Mock artefacts - no pending artefacts
        mock_artefacts.return_value = "No pending artefacts found"
        
        result = self.plugin.digest(self.msg, [])
        
        # Verify the mocks were called
        mock_get_github.assert_called_once_with("testuser")
        mock_generate_digest.assert_called_once()
        mock_artefacts.assert_called_once()
        
        # Check the result
        self.assertEqual(result, "Test digest content")


class TestCertificationHelperMethods(unittest.TestCase):
    """Test cases for helper methods"""

    def setUp(self):
        """Set up test fixtures"""
        bot = MagicMock()
        # Mock the PullRequestCache to prevent real API calls
        with patch('plugins.certification.certification.PullRequestCache'):
            self.plugin = CertificationPlugin(bot, "CertificationPlugin")
        # Mock the pr_cache methods
        self.plugin.pr_cache = MagicMock()

    def test_format_story_points(self):
        """Test _format_story_points helper"""
        self.assertEqual(self.plugin._format_story_points(5), " (5 story points)")
        self.assertEqual(self.plugin._format_story_points(1), " (1 story point)")
        self.assertEqual(self.plugin._format_story_points(0), "")
        self.assertEqual(self.plugin._format_story_points(None), "")

    @patch("plugins.certification.certification.get_email_from_mattermost_handle")
    @patch("plugins.certification.certification.get_github_username_from_mattermost_handle")
    def test_get_github_username_for_user(self, mock_get_github, mock_get_email):
        """Test _get_github_username_for_user helper"""
        # Mock the LDAP lookup to return a GitHub username directly
        mock_get_github.return_value = "github_user"
        mock_get_email.return_value = None  # Should not be called if first lookup succeeds
        
        result = self.plugin._get_github_username_for_user("mattermost_user")
        
        self.assertEqual(result, "github_user")
        mock_get_github.assert_called_once_with("mattermost_user")
        # Email lookup should not be called since first lookup succeeded
        mock_get_email.assert_not_called()

    def test_format_pr_summary_empty(self):
        """Test _format_pr_summary with no PRs"""
        pr_data = {
            "assigned": [],
            "authored_unassigned": [],
            "authored_approved": [],
            "authored_changes_requested": [],
            "authored_pending_review": [],
            "authored_unknown_status": []
        }
        
        result = self.plugin._format_pr_summary("testuser", pr_data, is_digest=False)
        
        self.assertIn("You have no PRs", result)

    def test_format_pr_summary_with_prs(self):
        """Test _format_pr_summary with PRs"""
        pr_data = {
            "assigned": [
                {
                    "title": "Assigned PR",
                    "html_url": "http://github.com/pr1",
                    "repository": "repo1",
                    "user_role": ["reviewer"]
                }
            ],
            "authored_unassigned": [],
            "authored_approved": [],
            "authored_changes_requested": [],
            "authored_pending_review": [],
            "authored_unknown_status": []
        }
        
        result = self.plugin._format_pr_summary("testuser", pr_data, is_digest=False)
        
        self.assertIn("PRs pending your review", result)
        self.assertIn("Assigned PR", result)
        self.assertIn("reviewer", result)


if __name__ == "__main__":
    unittest.main()