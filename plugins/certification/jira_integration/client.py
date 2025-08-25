"""
Jira client configuration and initialization
"""

import logging
import os
from typing import Optional

from jira import JIRA
from jira.exceptions import JIRAError

logger = logging.getLogger(__name__)

JIRA_SERVER = os.environ.get("JIRA_SERVER")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_FILTER_ID = os.environ.get("JIRA_FILTER_ID")


def get_jira_client() -> Optional[JIRA]:
    """
    Get authenticated Jira client

    Returns:
        Authenticated JIRA client or None if configuration is missing
    """
    if not all([JIRA_SERVER, JIRA_TOKEN, JIRA_EMAIL]):
        logger.warning(
            "Jira configuration incomplete. Need JIRA_SERVER, JIRA_TOKEN, and JIRA_EMAIL"
        )
        return None

    try:
        return JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))
    except JIRAError as e:
        logger.error(f"Failed to create Jira client: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error creating Jira client: {str(e)}")
        return None


def identify_story_points_field(client: Optional[JIRA] = None) -> Optional[str]:
    """
    Identify the custom field ID for story points in Jira

    Args:
        client: Optional JIRA client instance. If not provided, will create one.

    Returns:
        Field ID for story points (e.g., 'customfield_10024') or None if not found
    """
    if client is None:
        client = get_jira_client()
        if not client:
            return None

    try:
        fields = client.fields()

        story_points_names = ["story points", "story point", "storypoints", "sp"]

        for field in fields:
            if "custom" in field["id"]:
                field_name = field.get("name", "").lower()
                if any(sp_name in field_name for sp_name in story_points_names):
                    logger.info(f"Found story points field: {field['id']} - {field['name']}")
                    return field["id"]

        logger.warning("Story points field not found by name, using default customfield_10024")
        return "customfield_10024"

    except JIRAError as e:
        logger.error(f"Failed to identify story points field: {str(e)}")
        return None