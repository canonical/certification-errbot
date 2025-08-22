import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from test_observer.models import ArtefactResponse, ArtefactStatus

from plugins.certification.artefacts import (
    artefacts_by_user_handle,
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

        result = reply_with_artefacts_summary(self.user, ["assigned-to:testuser"])
        self.assertIn("**@testuser**", result)
        self.assertIn(
            "**[Artefact 1 1.0](https://test-observer.canonical.com/#/family1s/1)**",
            result,
        )
        self.assertNotIn(
            "**[Artefact 2 1.0](https://test-observer.canonical.com/#/family2s/2)**",
            result,
        )

    # Add more tests for different scenarios


class TestArtefactsSummarySending(ArtefactsTestBase):
    @patch("plugins.certification.artefacts.pending_artefacts_by_user_handle")
    def test_artefacts_digest(self, mock_pending_artefacts_by_user_handle):
        mock_pending_artefacts_by_user_handle.return_value = {
            "testuser": [self.artefact1]
        }

        sender = MagicMock()
        sender.build_identifier.return_value = "@testuser"

        send_artefact_summaries(sender)

        sent_message = sender.send.call_args[0][1]
        self.assertIn("Hello @testuser!", sent_message)
        self.assertIn("You have some test artefacts to review:", sent_message)
        self.assertIn(
            "**[Artefact 1 1.0](https://test-observer.canonical.com/#/family1s/1)**",
            sent_message,
        )
        self.assertNotIn(
            "**[Artefact 2 1.0](https://test-observer.canonical.com/#/family2s/2)**",
            sent_message,
        )


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


class TestFormatArtefactMessage(ArtefactsTestBase):
    def test_format_artefact_message_with_due_date(self):
        """Test formatting artefact message with due date"""
        result = format_artefact_message(self.artefact1)
        
        self.assertIn("Artefact 1 1.0", result)
        self.assertIn("https://test-observer.canonical.com/#/family1s/1", result)
        self.assertIn("(due", result)
        self.assertIn("1/2 reviews (50%)", result)

    def test_format_artefact_message_without_due_date(self):
        """Test formatting artefact message without due date"""
        self.artefact1.due_date = None
        result = format_artefact_message(self.artefact1)
        
        self.assertIn("Artefact 1 1.0", result)
        self.assertNotIn("(due", result)
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
    @patch("plugins.certification.artefacts.get_user_handle")
    def test_reply_with_assigned_to_filter(self, mock_get_user_handle, mock_get_artefacts, MockTestObserverClient):
        """Test reply_with_artefacts_summary with assigned-to filter"""
        mock_get_user_handle.return_value = {"username": "testuser"}
        mock_get_artefacts.return_value.parsed = [self.artefact1]
        
        result = reply_with_artefacts_summary(self.user, ["assigned-to:testuser"])
        
        self.assertIn("**@testuser**", result)
        self.assertIn("Artefact 1", result)

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
        self.assertEqual(result, "You can't use 'all' with 'name-contains' or 'assigned-to'")
        
        result = reply_with_artefacts_summary(self.user, ["all", "pending"])
        self.assertEqual(result, "You can't use 'all' with 'pending'")
        
        result = reply_with_artefacts_summary(self.user, ["name-contains:a", "name-contains:b"])
        self.assertEqual(result, "You can't use multiple 'name-contains' arguments")
        
        result = reply_with_artefacts_summary(self.user, ["assigned-to:user1", "assigned-to:user2"])
        self.assertEqual(result, "You can't use multiple 'assigned-to' arguments")

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
        self.assertIn("You have some test artefacts to review:", sent_message)
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


if __name__ == "__main__":
    unittest.main()
