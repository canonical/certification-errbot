import unittest
from unittest.mock import patch, MagicMock

from datetime import datetime, timedelta
from plugins.certification.artefacts import (
    reply_with_artefacts_summary,
    send_artefact_summaries,
    artefacts_by_user_handle,
)
from plugins.certification.test_observer.models import ArtefactStatus, ArtefactResponse


class ArtefactsTestBase(unittest.TestCase):
    def setUp(self):
        self.user = MagicMock(username="testuser", email="testuser@example.com")
        self.assignee = MagicMock(launchpad_email="testuser@example.com")

        self.artefact1 = ArtefactResponse(
            id=1,
            name="Artefact 1",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=self.assignee,
            completed_environment_reviews_count=1,
            all_environment_reviews_count=2,
            family="family1",
            track="track1",
            store="store1",
            series="series1",
            repo="repo1",
            os="os1",
            release="release1",
            owner="owner1",
            sha256="sha256",
            image_url="image_url",
            stage="stage1",
            bug_link="bug_link",
            created_at=datetime.now().date() - timedelta(days=10),
        )

        self.artefact2 = ArtefactResponse(
            id=2,
            name="Artefact 2",
            version="1.0",
            status=ArtefactStatus.MARKED_AS_FAILED,
            due_date=datetime.now().date() - timedelta(days=10),
            assignee=self.assignee,
            completed_environment_reviews_count=0,
            all_environment_reviews_count=1,
            family="family2",
            track="track2",
            store="store2",
            series="series2",
            repo="repo2",
            os="os2",
            release="release2",
            owner="owner2",
            sha256="sha2562",
            image_url="image_url2",
            stage="stage2",
            bug_link="bug_link2",
            created_at=datetime.now().date() - timedelta(days=10),
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


if __name__ == "__main__":
    unittest.main()
