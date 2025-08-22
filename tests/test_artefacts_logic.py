import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from test_observer.models import ArtefactResponse, ArtefactStatus

from plugins.certification.artefacts import (
    artefacts_by_user_handle,
    extract_artefact_id_from_url,
    format_artefact_message,
    pending_artefacts_by_user_handle,
    reply_with_artefacts_summary,
    send_artefact_summaries,
)


class ArtefactsTestBase(unittest.TestCase):
    def setUp(self):
        self.user = MagicMock(username="testuser", email="testuser@example.com")
        self.assignee = MagicMock(launchpad_email="testuser@example.com")

        self.artefact1 = ArtefactResponse(
            id=1,
            name="Artefact 1",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=self.assignee,
            completed_environment_reviews_count=1,
            all_environment_reviews_count=2,
            family="family1",
            track="track1",
            store="store1",
            branch="branch1",
            series="series1",
            repo="repo1",
            source="source1",
            os="os1",
            release="release1",
            owner="owner1",
            sha256="sha256",
            image_url="image_url",
            stage="stage1",
            bug_link="bug_link",
            comment="test comment 1",
            created_at=datetime.now() - timedelta(days=10),
        )

        self.artefact2 = ArtefactResponse(
            id=2,
            name="Artefact 2",
            version="1.0",
            status=ArtefactStatus.MARKED_AS_FAILED,
            archived=False,
            due_date=datetime.now().date() - timedelta(days=10),
            assignee=self.assignee,
            completed_environment_reviews_count=0,
            all_environment_reviews_count=1,
            family="family2",
            track="track2",
            store="store2",
            branch="branch2",
            series="series2",
            repo="repo2",
            source="source2",
            os="os2",
            release="release2",
            owner="owner2",
            sha256="sha2562",
            image_url="image_url2",
            stage="stage2",
            bug_link="bug_link2",
            comment="test comment 2",
            created_at=datetime.now() - timedelta(days=10),
        )


class TestArtefactsSummary(ArtefactsTestBase):
    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_artefacts_summary(
        self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient
    ):
        mock_get_user_handle.return_value = {"username": "testuser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1, self.artefact2]

        result = reply_with_artefacts_summary(self.user, ["testuser"])
        self.assertIn("**@testuser**", result)
        self.assertIn("## Artefact Review", result)
        self.assertIn("You have some Test Observer artefacts to review", result)
        self.assertIn("artefact review instructions", result)
        self.assertIn("https://certification.canonical.com/docs/ops/common-policies-docs/how-to/artefact-signoff-process/", result)
        self.assertIn(
            "**[Artefact 1 1.0](https://test-observer.canonical.com/#/family1s/1)**",
            result,
        )
        self.assertNotIn(
            "**[Artefact 2 1.0](https://test-observer.canonical.com/#/family2s/2)**",
            result,
        )

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_artefacts_summary_no_args_finds_user(
        self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient
    ):
        """Test that argumentless call finds artefacts for the sender"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1]

        # When no args, should find artefacts for sender
        result = reply_with_artefacts_summary(self.user, [])
        self.assertIn("**@testuser**", result)
        self.assertIn("Artefact 1", result)

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_artefacts_summary_no_args_case_insensitive(
        self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient
    ):
        """Test that argumentless call finds artefacts with case-insensitive match"""
        # User handle from LDAP returns different case
        mock_get_user_handle.return_value = {"username": "TestUser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1]
        
        # But sender has lowercase username
        self.user.username = "testuser"

        # Should still find artefacts due to case-insensitive match
        result = reply_with_artefacts_summary(self.user, [])
        self.assertIn("TestUser", result)  # Will use the actual key from artefacts_by_user
        self.assertIn("Artefact 1", result)

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_artefacts_summary_no_args_no_artefacts(
        self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient
    ):
        """Test that argumentless call shows appropriate message when user has no artefacts"""
        mock_get_user_handle.return_value = {"username": "otheruser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1]  # Assigned to otheruser
        
        # Sender is testuser but artefacts are for otheruser
        result = reply_with_artefacts_summary(self.user, [])
        self.assertIn("No pending artefacts found for @testuser", result)

    # Add more tests for different scenarios


class TestArtefactsSummarySending(ArtefactsTestBase):
    @patch("plugins.certification.artefacts.pending_artefacts_by_user_handle")
    def test_artefacts_digest(self, mock_pending_artefacts_by_user_handle):
        # Include both overdue and upcoming artefacts
        overdue_artefact = ArtefactResponse(
            id=3,
            name="Overdue Artefact",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() - timedelta(days=3),  # Overdue
            assignee=self.assignee,
            completed_environment_reviews_count=0,
            all_environment_reviews_count=1,
            family="snap",
            track="track3",
            store="store3",
            branch="branch3",
            series="series3",
            repo="repo3",
            source="source3",
            os="os3",
            release="release3",
            owner="owner3",
            sha256="sha2563",
            image_url="image_url3",
            stage="stage3",
            bug_link="bug_link3",
            comment="test comment 3",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        mock_pending_artefacts_by_user_handle.return_value = {
            "testuser": [self.artefact1, overdue_artefact]
        }

        sender = MagicMock()
        sender.build_identifier.return_value = "@testuser"

        send_artefact_summaries(sender)

        sent_message = sender.send.call_args[0][1]
        self.assertIn("Hello @testuser!", sent_message)
        # Check for section heading and review instructions link
        self.assertIn("## Artefact Review", sent_message)
        self.assertIn("You have some Test Observer artefacts to review", sent_message)
        self.assertIn("artefact review instructions", sent_message)
        self.assertIn("https://certification.canonical.com/docs/ops/common-policies-docs/how-to/artefact-signoff-process/", sent_message)
        # Check that overdue artefact is present with overdue indicator
        self.assertIn("Overdue Artefact", sent_message)
        self.assertIn("🔴", sent_message)
        self.assertIn("OVERDUE", sent_message)
        self.assertIn("Artefact 1", sent_message)


class TestArtefactsByUserHandle(ArtefactsTestBase):
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_artefacts_by_user_handle(self, mock_get_user_handle):
        mock_get_user_handle.return_value = {"username": "testuser"}

        artefacts_response = [self.artefact1, self.artefact2]
        result = artefacts_by_user_handle(artefacts_response, None, None, False)

        self.assertIn("testuser", result)
        self.assertEqual(len(result["testuser"]), 1)
        self.assertEqual(result["testuser"][0].id, 1)

    @patch("plugins.certification.artefacts.get_user_handle")
    def test_artefacts_by_user_handle_with_filter(self, mock_get_user_handle):
        mock_get_user_handle.return_value = {"username": "testuser"}

        artefacts_response = [self.artefact1, self.artefact2]
        result = artefacts_by_user_handle(artefacts_response, "artefact 1", None, False)

        self.assertIn("testuser", result)
        self.assertEqual(len(result["testuser"]), 1)
        self.assertEqual(result["testuser"][0].id, 1)

        result = artefacts_by_user_handle(artefacts_response, "artefact 2", None, False)
        self.assertNotIn("testuser", result)

    @patch("plugins.certification.artefacts.get_user_handle")
    def test_artefacts_by_user_handle_with_assigned_to_filter(
        self, mock_get_user_handle
    ):
        mock_get_user_handle.return_value = {"username": "testuser"}

        artefacts_response = [self.artefact1, self.artefact2]
        result = artefacts_by_user_handle(artefacts_response, None, "testuser", False)

        self.assertIn("testuser", result)
        self.assertEqual(len(result["testuser"]), 1)
        self.assertEqual(result["testuser"][0].id, 1)

        result = artefacts_by_user_handle(artefacts_response, None, "otheruser", False)
        self.assertNotIn("testuser", result)

    @patch("plugins.certification.artefacts.get_user_handle")
    def test_artefacts_by_user_handle_with_pending_filter(self, mock_get_user_handle):
        mock_get_user_handle.return_value = {"username": "testuser"}

        artefacts_response = [self.artefact1, self.artefact2]
        result = artefacts_by_user_handle(artefacts_response, None, None, True)

        self.assertIn("testuser", result)
        self.assertEqual(len(result["testuser"]), 1)
        self.assertEqual(result["testuser"][0].id, 1)

    @patch("plugins.certification.artefacts.get_user_handle")
    @patch("plugins.certification.artefacts.INCLUDED_FAMILIES", {"snap", "deb", "image"})
    def test_filters_by_configured_families(self, mock_get_user_handle):
        """Test that artefacts are filtered by configured families"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        
        # Create a charm artefact that should be excluded when families are configured
        charm_artefact = ArtefactResponse(
            id=10,
            name="Charm Artefact",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=self.assignee,
            completed_environment_reviews_count=1,
            all_environment_reviews_count=2,
            family="charm",  # Charm family - not in configured list
            track="track10",
            store="store10",
            branch="branch10",
            series="series10",
            repo="repo10",
            source="source10",
            os="os10",
            release="release10",
            owner="owner10",
            sha256="sha25610",
            image_url="image_url10",
            stage="stage10",
            bug_link="bug_link10",
            comment="test comment 10",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        # Test with both included and excluded families
        # artefact1 has family="family1" which is not in the configured list
        # but we'll create a snap artefact that should be included
        snap_artefact = ArtefactResponse(
            id=11,
            name="Snap Artefact",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=self.assignee,
            completed_environment_reviews_count=1,
            all_environment_reviews_count=2,
            family="snap",  # Snap family - in configured list
            track="track11",
            store="store11",
            branch="branch11",
            series="series11",
            repo="repo11",
            source="source11",
            os="os11",
            release="release11",
            owner="owner11",
            sha256="sha25611",
            image_url="image_url11",
            stage="stage11",
            bug_link="bug_link11",
            comment="test comment 11",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        artefacts_response = [charm_artefact, snap_artefact]
        result = artefacts_by_user_handle(artefacts_response, None, None, False)
        
        # Should only include snap artefact
        self.assertIn("testuser", result)
        self.assertEqual(len(result["testuser"]), 1)
        self.assertEqual(result["testuser"][0].id, 11)
        self.assertEqual(result["testuser"][0].family, "snap")
    
    @patch("plugins.certification.artefacts.get_user_handle")
    @patch("plugins.certification.artefacts.INCLUDED_FAMILIES", None)
    def test_includes_all_families_when_not_configured(self, mock_get_user_handle):
        """Test that all families are included when INCLUDED_FAMILIES is None"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        
        # Create artefacts with different families
        charm_artefact = ArtefactResponse(
            id=10,
            name="Charm Artefact",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=self.assignee,
            completed_environment_reviews_count=1,
            all_environment_reviews_count=2,
            family="charm",
            track="track10",
            store="store10",
            branch="branch10",
            series="series10",
            repo="repo10",
            source="source10",
            os="os10",
            release="release10",
            owner="owner10",
            sha256="sha25610",
            image_url="image_url10",
            stage="stage10",
            bug_link="bug_link10",
            comment="test comment 10",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        artefacts_response = [self.artefact1, charm_artefact]
        result = artefacts_by_user_handle(artefacts_response, None, None, False)
        
        # Should include both artefacts when no filtering is configured
        self.assertIn("testuser", result)
        self.assertEqual(len(result["testuser"]), 2)
        artefact_ids = {a.id for a in result["testuser"]}
        self.assertEqual(artefact_ids, {1, 10})


class TestFormatArtefactMessage(ArtefactsTestBase):
    def test_format_artefact_message_with_due_date(self):
        """Test formatting artefact message with due date"""
        # Set due date to future (not urgent)
        self.artefact1.due_date = datetime.now().date() + timedelta(days=10)
        result = format_artefact_message(self.artefact1)
        
        self.assertIn("Artefact 1 1.0", result)
        self.assertIn("https://test-observer.canonical.com/#/family1s/1", result)
        self.assertIn("(due", result)
        self.assertIn("1/2 reviews (50%)", result)
        # Should not have warning emoji for far future date
        self.assertNotIn("⚠️", result)
        self.assertNotIn("🔴", result)

    def test_format_artefact_message_due_soon(self):
        """Test formatting when artefact is due within 7 days"""
        self.artefact1.due_date = datetime.now().date() + timedelta(days=3)
        result = format_artefact_message(self.artefact1)
        
        self.assertIn("Artefact 1 1.0", result)
        self.assertIn("⚠️ Due in 3 days", result)
        self.assertIn("1/2 reviews (50%)", result)

    def test_format_artefact_message_overdue(self):
        """Test formatting when artefact is overdue"""
        self.artefact1.due_date = datetime.now().date() - timedelta(days=5)
        result = format_artefact_message(self.artefact1, is_overdue=True)
        
        self.assertIn("Artefact 1 1.0", result)
        self.assertIn("🔴", result)
        self.assertIn("OVERDUE by 5 days", result)
        self.assertIn("1/2 reviews (50%)", result)

    def test_format_artefact_message_without_due_date(self):
        """Test formatting artefact message without due date"""
        self.artefact1.due_date = None
        result = format_artefact_message(self.artefact1)
        
        self.assertIn("Artefact 1 1.0", result)
        self.assertNotIn("(due", result)
        self.assertNotIn("⚠️", result)
        self.assertNotIn("🔴", result)
        self.assertIn("1/2 reviews (50%)", result)

    def test_format_artefact_message_zero_reviews(self):
        """Test formatting when no reviews are completed"""
        self.artefact2.completed_environment_reviews_count = 0
        self.artefact2.all_environment_reviews_count = 0
        result = format_artefact_message(self.artefact2)
        
        self.assertIn("0/0 reviews (0%)", result)


class TestReplyWithArtefactsSummary(ArtefactsTestBase):
    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_reply_with_all_artefacts(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary with 'all' argument"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1]
        
        result = reply_with_artefacts_summary(self.user, ["all"])
        
        self.assertIn("**@testuser**", result)
        self.assertIn("Artefact 1", result)

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_reply_with_name_filter(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary with name-contains filter"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1, self.artefact2]
        
        result = reply_with_artefacts_summary(self.user, ["name-contains:artefact 1"])
        
        self.assertIn("Artefact 1", result)
        self.assertNotIn("Artefact 2", result)


    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    def test_reply_with_no_artefacts(self, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary when no artefacts match"""
        mock_get_artefacts.return_value.parsed = []
        
        result = reply_with_artefacts_summary(self.user, [])
        
        self.assertIn("No pending artefacts", result)

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    def test_reply_with_api_error(self, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary when API returns non-list"""
        mock_get_artefacts.return_value.parsed = "not a list"
        
        result = reply_with_artefacts_summary(self.user, [])
        
        self.assertEqual(result, "Error retrieving artefacts")

    def test_reply_with_invalid_argument_combinations(self):
        """Test reply_with_artefacts_summary with invalid argument combinations"""
        result = reply_with_artefacts_summary(self.user, ["all", "name-contains:test"])
        self.assertEqual(result, "You can't use 'all' with 'name-contains' or username filter")
        
        result = reply_with_artefacts_summary(self.user, ["all", "pending"])
        self.assertEqual(result, "You can't use 'all' with 'pending'")
        
        result = reply_with_artefacts_summary(self.user, ["name-contains:a", "name-contains:b"])
        self.assertEqual(result, "You can't use multiple 'name-contains' arguments")

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_reply_with_pending_filter(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary with pending filter"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1, self.artefact2]
        
        result = reply_with_artefacts_summary(self.user, ["pending"])
        
        self.assertIn("Artefact 1", result)
        self.assertNotIn("Artefact 2", result)

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_reply_with_direct_username(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary with direct username (no assigned-to prefix)"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1]
        
        # Test with direct username
        result = reply_with_artefacts_summary(self.user, ["testuser"])
        self.assertIn("**@testuser**", result)
        self.assertIn("Artefact 1", result)
        
        # Test with @ prefix
        result = reply_with_artefacts_summary(self.user, ["@testuser"])
        self.assertIn("**@testuser**", result)
        self.assertIn("Artefact 1", result)
    
    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_reply_with_overdue_and_current_artefacts(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary formats overdue and current artefacts correctly"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        
        # Create overdue artefact
        overdue_artefact = ArtefactResponse(
            id=3,
            name="Overdue Artefact",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() - timedelta(days=3),
            assignee=self.assignee,
            completed_environment_reviews_count=0,
            all_environment_reviews_count=1,
            family="snap",
            track="track3",
            store="store3",
            branch="branch3",
            series="series3",
            repo="repo3",
            source="source3",
            os="os3",
            release="release3",
            owner="owner3",
            sha256="sha2563",
            image_url="image_url3",
            stage="stage3",
            bug_link="bug_link3",
            comment="test comment 3",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        mock_get_artefacts.return_value.parsed = [self.artefact1, overdue_artefact]
        
        result = reply_with_artefacts_summary(self.user, [])
        
        # Check single heading and review instructions
        self.assertIn("## Artefact Review", result)
        self.assertEqual(result.count("## Artefact Review"), 1)
        self.assertIn("You have some Test Observer artefacts to review", result)
        self.assertIn("artefact review instructions", result)
        self.assertIn("https://certification.canonical.com/docs/ops/common-policies-docs/how-to/artefact-signoff-process/", result)
        
        # Check overdue comes first
        self.assertIn("🔴", result)
        self.assertIn("OVERDUE by 3 days", result)
        self.assertIn("Overdue Artefact", result)
        
        # Check current artefact is present
        self.assertIn("Artefact 1", result)
        
        # Verify order (overdue should come before current)
        overdue_pos = result.index("Overdue Artefact")
        current_pos = result.index("Artefact 1")
        self.assertLess(overdue_pos, current_pos)

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    @patch("plugins.certification.artefacts.INCLUDED_FAMILIES", {"snap", "deb"})
    def test_reply_filters_by_configured_families(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary filters by configured families"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        
        # Create artefacts with different families
        snap_artefact = ArtefactResponse(
            id=10,
            name="Snap Artefact",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=self.assignee,
            completed_environment_reviews_count=1,
            all_environment_reviews_count=2,
            family="snap",  # Included family
            track="track10",
            store="store10",
            branch="branch10",
            series="series10",
            repo="repo10",
            source="source10",
            os="os10",
            release="release10",
            owner="owner10",
            sha256="sha25610",
            image_url="image_url10",
            stage="stage10",
            bug_link="bug_link10",
            comment="test comment 10",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        charm_artefact = ArtefactResponse(
            id=11,
            name="Charm Artefact",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=self.assignee,
            completed_environment_reviews_count=1,
            all_environment_reviews_count=2,
            family="charm",  # Not included family
            track="track11",
            store="store11",
            branch="branch11",
            series="series11",
            repo="repo11",
            source="source11",
            os="os11",
            release="release11",
            owner="owner11",
            sha256="sha25611",
            image_url="image_url11",
            stage="stage11",
            bug_link="bug_link11",
            comment="test comment 11",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        mock_get_artefacts.return_value.parsed = [snap_artefact, charm_artefact]
        
        result = reply_with_artefacts_summary(self.user, [])
        
        # Should only show snap artefact
        self.assertIn("Snap Artefact", result)
        self.assertNotIn("Charm Artefact", result)

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_reply_with_unassigned_artefacts(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary with unassigned artefacts"""
        mock_get_user_handle.return_value = None
        
        # Create unassigned artefact
        unassigned_artefact = ArtefactResponse(
            id=3,
            name="Unassigned Artefact",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=None,
            completed_environment_reviews_count=0,
            all_environment_reviews_count=1,
            family="family3",
            track="track3",
            store="store3",
            branch="branch3",
            series="series3",
            repo="repo3",
            source="source3",
            os="os3",
            release="release3",
            owner="owner3",
            sha256="sha2563",
            image_url="image_url3",
            stage="stage3",
            bug_link="bug_link3",
            comment="test comment 3",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        mock_get_artefacts.return_value.parsed = [unassigned_artefact]
        
        result = reply_with_artefacts_summary(self.user, ["all"])
        
        self.assertIn("**No assignee**", result)
        self.assertIn("Unassigned Artefact", result)


class TestPendingArtefactsByUserHandle(ArtefactsTestBase):
    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_pending_artefacts_by_user_handle(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test pending_artefacts_by_user_handle returns only pending artefacts"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        
        # Create approved artefact that should be filtered out
        approved_artefact = ArtefactResponse(
            id=3,
            name="Approved Artefact",
            version="1.0",
            status=ArtefactStatus.APPROVED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=self.assignee,
            completed_environment_reviews_count=2,
            all_environment_reviews_count=2,
            family="family3",
            track="track3",
            store="store3",
            branch="branch3",
            series="series3",
            repo="repo3",
            source="source3",
            os="os3",
            release="release3",
            owner="owner3",
            sha256="sha2563",
            image_url="image_url3",
            stage="stage3",
            bug_link="bug_link3",
            comment="test comment 3",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        mock_get_artefacts.return_value.parsed = [self.artefact1, self.artefact2, approved_artefact]
        
        result = pending_artefacts_by_user_handle()
        
        self.assertIn("testuser", result)
        self.assertEqual(len(result["testuser"]), 1)
        self.assertEqual(result["testuser"][0].id, 1)

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    def test_pending_artefacts_by_user_handle_api_error(self, mock_get_artefacts, MockTestObserverClient):
        """Test pending_artefacts_by_user_handle raises exception on API error"""
        mock_get_artefacts.return_value.parsed = "not a list"
        
        with self.assertRaises(Exception) as context:
            pending_artefacts_by_user_handle()
        
        self.assertEqual(str(context.exception), "Error retrieving artefacts")

    @patch("plugins.certification.artefacts.TestObserverClient")
    @patch("plugins.certification.artefacts.get_artefacts")
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_pending_artefacts_excludes_no_assignee_no_due_date(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test that artefacts with no assignee and no due date are excluded"""
        mock_get_user_handle.return_value = None
        
        # Create artefact with no assignee and no due date
        no_assignee_no_due_date = ArtefactResponse(
            id=4,
            name="No Assignee No Due Date",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=None,
            assignee=None,
            completed_environment_reviews_count=0,
            all_environment_reviews_count=1,
            family="family4",
            track="track4",
            store="store4",
            branch="branch4",
            series="series4",
            repo="repo4",
            source="source4",
            os="os4",
            release="release4",
            owner="owner4",
            sha256="sha2564",
            image_url="image_url4",
            stage="stage4",
            bug_link="bug_link4",
            comment="test comment 4",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        mock_get_artefacts.return_value.parsed = [no_assignee_no_due_date]
        
        result = pending_artefacts_by_user_handle()
        
        self.assertEqual(len(result), 0)


class TestSendArtefactSummaries(ArtefactsTestBase):
    @patch("plugins.certification.artefacts.pending_artefacts_by_user_handle")
    def test_send_artefact_summaries_single_user(self, mock_pending_artefacts):
        """Test send_artefact_summaries sends messages to users with pending artefacts"""
        mock_pending_artefacts.return_value = {
            "testuser": [self.artefact1]
        }
        
        sender = MagicMock()
        sender.build_identifier.return_value = "@testuser"
        
        send_artefact_summaries(sender)
        
        sender.build_identifier.assert_called_once_with("@testuser")
        sender.send.assert_called_once()
        
        sent_message = sender.send.call_args[0][1]
        self.assertIn("Hello @testuser!", sent_message)
        self.assertIn("## Artefact Review", sent_message)
        self.assertIn("You have some Test Observer artefacts to review", sent_message)
        self.assertIn("artefact review instructions", sent_message)
        self.assertIn("https://certification.canonical.com/docs/ops/common-policies-docs/how-to/artefact-signoff-process/", sent_message)
        self.assertIn("Artefact 1", sent_message)

    @patch("plugins.certification.artefacts.pending_artefacts_by_user_handle")
    def test_send_artefact_summaries_multiple_users(self, mock_pending_artefacts):
        """Test send_artefact_summaries sends messages to multiple users"""
        artefact3 = ArtefactResponse(
            id=3,
            name="Artefact 3",
            version="2.0",
            status=ArtefactStatus.UNDECIDED,
            archived=False,
            due_date=datetime.now().date() + timedelta(days=2),
            assignee=MagicMock(launchpad_email="otheruser@example.com"),
            completed_environment_reviews_count=0,
            all_environment_reviews_count=3,
            family="family3",
            track="track3",
            store="store3",
            branch="branch3",
            series="series3",
            repo="repo3",
            source="source3",
            os="os3",
            release="release3",
            owner="owner3",
            sha256="sha2563",
            image_url="image_url3",
            stage="stage3",
            bug_link="bug_link3",
            comment="test comment 3",
            created_at=datetime.now() - timedelta(days=10),
        )
        
        mock_pending_artefacts.return_value = {
            "testuser": [self.artefact1],
            "otheruser": [artefact3]
        }
        
        sender = MagicMock()
        sender.build_identifier.side_effect = lambda x: x
        
        send_artefact_summaries(sender)
        
        self.assertEqual(sender.send.call_count, 2)
        
        # Check both messages were sent
        calls = sender.send.call_args_list
        messages = [call[0][1] for call in calls]
        
        self.assertTrue(any("@testuser" in msg for msg in messages))
        self.assertTrue(any("@otheruser" in msg for msg in messages))
        self.assertTrue(any("Artefact 1" in msg for msg in messages))
        self.assertTrue(any("Artefact 3" in msg for msg in messages))

    @patch("plugins.certification.artefacts.pending_artefacts_by_user_handle")
    def test_send_artefact_summaries_no_artefacts(self, mock_pending_artefacts):
        """Test send_artefact_summaries does not send messages when no artefacts"""
        mock_pending_artefacts.return_value = {}
        
        sender = MagicMock()
        
        send_artefact_summaries(sender)
        
        sender.send.assert_not_called()

    @patch("plugins.certification.artefacts.pending_artefacts_by_user_handle")
    def test_send_artefact_summaries_empty_user_list(self, mock_pending_artefacts):
        """Test send_artefact_summaries handles users with empty artefact lists"""
        mock_pending_artefacts.return_value = {
            "testuser": []
        }
        
        sender = MagicMock()
        
        send_artefact_summaries(sender)
        
        sender.send.assert_not_called()

    @patch("plugins.certification.artefacts.pending_artefacts_by_user_handle")
    def test_send_artefact_summaries_none_user(self, mock_pending_artefacts):
        """Test send_artefact_summaries skips None users"""
        mock_pending_artefacts.return_value = {
            None: [self.artefact1]
        }
        
        sender = MagicMock()
        
        send_artefact_summaries(sender)
        
        sender.send.assert_not_called()


class TestExtractArtefactIdFromUrl(unittest.TestCase):
    def test_extract_id_from_integer_string(self):
        """Test extracting ID when given an integer as string"""
        self.assertEqual(extract_artefact_id_from_url("123"), 123)
        self.assertEqual(extract_artefact_id_from_url("456"), 456)
        self.assertEqual(extract_artefact_id_from_url("0"), 0)

    def test_extract_id_from_snap_url(self):
        """Test extracting ID from snap URLs"""
        self.assertEqual(
            extract_artefact_id_from_url("https://test-observer.canonical.com/#/snaps/123"),
            123
        )
        self.assertEqual(
            extract_artefact_id_from_url("https://test-observer.canonical.com/#/snap/456"),
            456
        )
        
    def test_extract_id_from_deb_url(self):
        """Test extracting ID from deb URLs"""
        self.assertEqual(
            extract_artefact_id_from_url("https://test-observer.canonical.com/#/debs/789"),
            789
        )
        self.assertEqual(
            extract_artefact_id_from_url("https://test-observer.canonical.com/#/deb/321"),
            321
        )
        
    def test_extract_id_from_image_url(self):
        """Test extracting ID from image URLs"""
        self.assertEqual(
            extract_artefact_id_from_url("https://test-observer.canonical.com/#/images/111"),
            111
        )
        self.assertEqual(
            extract_artefact_id_from_url("https://test-observer.canonical.com/#/image/222"),
            222
        )
        
    def test_extract_id_from_charm_url(self):
        """Test extracting ID from charm URLs"""
        self.assertEqual(
            extract_artefact_id_from_url("https://test-observer.canonical.com/#/charms/333"),
            333
        )
        self.assertEqual(
            extract_artefact_id_from_url("https://test-observer.canonical.com/#/charm/444"),
            444
        )
        
    def test_extract_id_from_partial_url(self):
        """Test extracting ID from partial URLs"""
        self.assertEqual(extract_artefact_id_from_url("#/snaps/555"), 555)
        self.assertEqual(extract_artefact_id_from_url("/#/debs/666"), 666)
        
    def test_invalid_input_raises_error(self):
        """Test that invalid inputs raise ValueError"""
        with self.assertRaises(ValueError) as context:
            extract_artefact_id_from_url("not-a-number")
        self.assertIn("Could not extract artefact ID from: not-a-number", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            extract_artefact_id_from_url("https://example.com/other/123")
        self.assertIn("Could not extract artefact ID from:", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            extract_artefact_id_from_url("#/snaps/abc")
        self.assertIn("Could not extract artefact ID from:", str(context.exception))
        
        with self.assertRaises(ValueError) as context:
            extract_artefact_id_from_url("")
        self.assertIn("Could not extract artefact ID from:", str(context.exception))


if __name__ == "__main__":
    unittest.main()
