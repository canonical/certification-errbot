import unittest
from unittest.mock import patch, MagicMock

from datetime import datetime, timedelta
from plugins.certification.artefacts import artefacts_summary
from plugins.certification.test_observer.models import ArtefactStatus, ArtefactResponse

class TestArtefactsSummary(unittest.TestCase):

    @patch('plugins.certification.artefacts.TestObserverClient')
    @patch('plugins.certification.artefacts.get_artefacts')
    @patch('plugins.certification.artefacts.get_assignee_handle')
    def test_artefacts_summary(self, mock_get_assignee_handle, mock_get_artefacts, MockTestObserverClient):
        user = MagicMock(username="testuser@example.com", email="testuser@example.com")
        assignee = MagicMock(launchpad_email="testuser@example.com")

        mock_get_assignee_handle.return_value = {"username": "testuser"}

        artefact1 = ArtefactResponse(
            id=1,
            name="Artefact 1",
            version="1.0",
            status=ArtefactStatus.UNDECIDED,
            due_date=datetime.now().date() + timedelta(days=1),
            assignee=assignee,
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
            bug_link="bug_link"
        )

        artefact2 = ArtefactResponse(
            id=2,
            name="Artefact 2",
            version="1.0",
            status=ArtefactStatus.MARKED_AS_FAILED,
            due_date=datetime.now().date() - timedelta(days=10),
            assignee=assignee,
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
            bug_link="bug_link2"
        )

        mock_get_artefacts.return_value.parsed = [artefact1, artefact2]

        result = artefacts_summary(user, ["assigned-to:testuser"])
        self.assertIn("**@testuser**", result)
        self.assertIn("**[Artefact 1 1.0](https://test-observer.canonical.com/#/family1s/1)**", result)
        self.assertNotIn("**[Artefact 2 1.0](https://test-observer.canonical.com/#/family2s/2)**", result)

    # Add more tests for different scenarios

if __name__ == '__main__':
    unittest.main()
