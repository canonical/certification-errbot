import logging
import os
from typing import Any, Dict, List, Optional

from jira import JIRA
from jira.exceptions import JIRAError
from ldap import get_email_from_github_username, get_email_from_mattermost_handle

logger = logging.getLogger(__name__)


def get_priority_sort_key(priority: str) -> int:
    """
    Convert Jira priority name to a numeric sort key.
    Lower numbers = higher priority (will be sorted first).
    """
    priority_mapping = {
        "highest": 1,
        "high": 2, 
        "medium": 3,
        "low": 4,
        "lowest": 5,
        "none": 6,
        "": 6,  # Empty priority treated as lowest
    }
    return priority_mapping.get(priority.lower(), 6)


def is_review_status(status_name: str) -> bool:
    """
    Determine if a Jira status indicates the issue is in review.
    Common review status names include variations of "review", "pending", etc.
    """
    if not status_name:
        return False
    
    status_lower = status_name.lower()
    review_keywords = [
        "review", "reviewing", "in review", "under review", "code review",
        "pending review", "waiting for review", "ready for review",
        "peer review", "technical review", "design review"
    ]
    
    return any(keyword in status_lower for keyword in review_keywords)


JIRA_SERVER = os.environ.get("JIRA_SERVER")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL")
JIRA_FILTER_ID = os.environ.get("JIRA_FILTER_ID")  # Optional saved filter ID

# Cache for Jira connections
_jira_client = None

# Simple cache for Jira issues mapped by assignee (similar to GitHub cache pattern)
jira_issues_cache: dict[
    str, list[dict[str, any]]
] = {}  # assignee email -> list of issues
jira_account_to_email: dict[str, str] = {}  # account ID -> email mapping


def get_jira_client() -> Optional[JIRA]:
    """Get authenticated Jira client instance"""
    global _jira_client

    if not all([JIRA_SERVER, JIRA_TOKEN, JIRA_EMAIL]):
        logger.warning(
            "Jira configuration incomplete - missing JIRA_SERVER, JIRA_TOKEN, or JIRA_EMAIL"
        )
        return None

    if _jira_client is None:
        try:
            _jira_client = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_TOKEN))
        except JIRAError as e:
            logger.error(f"Failed to initialize Jira client: {str(e)}")
            return None

    return _jira_client


def identify_story_points_field():
    """
    Helper function to identify the correct story points field in Jira
    Fetches a few issues and logs all fields to help identify the story points field
    """
    client = get_jira_client()
    if not client:
        logger.error("Failed to get Jira client for field identification")
        return
        
    try:
        # Get a few recent issues to analyze their fields
        issues = client.search_issues(
            jql_str="ORDER BY created DESC",
            maxResults=3,
            fields="*all"
        )
        
        if not issues:
            logger.warning("No issues found for field analysis")
            return
    except Exception as e:
        logger.error(f"Error during field identification: {str(e)}")


def refresh_jira_issues_cache():
    """
    Refresh the Jira issues cache by fetching all issues from the saved filter
    Similar to GitHub cache pattern - called from the main plugin when needed
    """
    if not JIRA_FILTER_ID:
        return

    client = get_jira_client()
    if not client:
        logger.error("Failed to get Jira client for cache refresh")
        return

    try:

        # Get the saved filter
        saved_filter = client.filter(JIRA_FILTER_ID)

        # Fetch all issues from the filter, optionally filtering by current sprint
        base_jql = saved_filter.jql
        sprint_filter = (
            os.environ.get("JIRA_CURRENT_SPRINT_ONLY", "false").lower() == "true"
        )

        if sprint_filter:
            # Remove ORDER BY from base JQL if present, add sprint filter, then add ORDER BY back
            if "ORDER BY" in base_jql.upper():
                jql_parts = base_jql.split("ORDER BY")
                jql = f"{jql_parts[0].strip()} AND sprint in openSprints() ORDER BY {jql_parts[1].strip()}"
            else:
                jql = f"{base_jql} AND sprint in openSprints()"
        else:
            jql = base_jql


        # Fetch all issues with pagination
        all_issues = []
        start_at = 0
        max_results = 100  # Reasonable page size

        while True:
            issues = client.search_issues(
                jql_str=jql,
                startAt=start_at,
                maxResults=max_results,
                fields="*all",  # Fetch all fields to identify story points field
            )

            if not issues:
                break

            all_issues.extend(issues)
            
            # If we got fewer results than requested, we're done
            if len(issues) < max_results:
                break

            start_at += max_results


        # Clear and rebuild the cache
        jira_issues_cache.clear()
        jira_account_to_email.clear()

        for issue in all_issues:
            # Extract assignee account ID and email
            if hasattr(issue.fields, "assignee") and issue.fields.assignee:
                account_id = issue.fields.assignee.accountId
                email = getattr(issue.fields.assignee, "emailAddress", account_id)

                # Store account ID to email mapping
                jira_account_to_email[account_id] = email

                # Use email as the cache key for consistency with existing code
                if email not in jira_issues_cache:
                    jira_issues_cache[email] = []

                # Get story points (customfield_10024 per user requirements)
                story_points = getattr(issue.fields, "customfield_10024", None)

                # Determine issue state based on status
                status_name = issue.fields.status.name
                status_category = getattr(issue.fields.status, "statusCategory", None)
                is_completed = (
                    status_category and status_category.name.lower() == "done"
                )
                is_in_review = is_review_status(status_name)

                jira_issues_cache[email].append(
                    {
                        "key": issue.key,
                        "summary": issue.fields.summary,
                        "status": status_name,
                        "priority": issue.fields.priority.name
                        if issue.fields.priority
                        else "None",
                        "story_points": story_points,
                        "is_completed": is_completed,
                        "is_in_review": is_in_review,
                        "url": f"{JIRA_SERVER}/browse/{issue.key}",
                    }
                )

        # Log assignee emails for debugging
        assignee_emails = list(jira_issues_cache.keys())

    except JIRAError as e:
        logger.error(f"Failed to refresh issues cache: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error refreshing cache: {str(e)}")


def get_jira_issues_for_user(
    email: str, max_results: int = 50
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get Jira issues assigned to a user by email address from cache
    Separates active, review, completed, and untriaged issues, sorted by priority

    Args:
        email: User's email address (account ID)
        max_results: Maximum number of issues to return per category

    Returns:
        Dictionary with 'active', 'review', 'completed', and 'untriaged' lists of issue dictionaries
    """
    if email in jira_issues_cache:
        cached_issues = jira_issues_cache[email]

        # Separate issues by state and priority
        # Untriaged = not completed AND (no priority OR priority is "None")
        untriaged_issues = [
            issue for issue in cached_issues 
            if not issue.get("is_completed", False) 
            and (not issue.get("priority") or issue.get("priority", "").lower() in ["none", ""])
        ]
        
        # Active = not completed, not in review, AND has valid priority
        active_issues = [
            issue for issue in cached_issues 
            if not issue.get("is_completed", False) 
            and not issue.get("is_in_review", False)
            and issue.get("priority") 
            and issue.get("priority", "").lower() not in ["none", ""]
        ]
        
        # Review = not completed, in review, AND has valid priority
        review_issues = [
            issue for issue in cached_issues 
            if not issue.get("is_completed", False) 
            and issue.get("is_in_review", False)
            and issue.get("priority") 
            and issue.get("priority", "").lower() not in ["none", ""]
        ]
        
        completed_issues = [
            issue for issue in cached_issues if issue.get("is_completed", False)
        ]

        # Sort by priority (highest priority first) and limit results
        active_sorted = sorted(
            active_issues, key=lambda x: get_priority_sort_key(x.get("priority", ""))
        )[:max_results]
        review_sorted = sorted(
            review_issues, key=lambda x: get_priority_sort_key(x.get("priority", ""))
        )[:max_results]
        completed_sorted = sorted(
            completed_issues, key=lambda x: get_priority_sort_key(x.get("priority", ""))
        )[:max_results]
        # Untriaged issues don't need priority sorting (they have no priority)
        untriaged_sorted = untriaged_issues[:max_results]

        result = {
            "active": active_sorted, 
            "review": review_sorted, 
            "completed": completed_sorted,
            "untriaged": untriaged_sorted
        }

        return result

    return {"active": [], "review": [], "completed": [], "untriaged": []}


def get_jira_issues_for_mattermost_handle(
    mattermost_handle: str, max_results: int = 50
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get Jira issues for a user by their Mattermost handle
    Uses LDAP lookup to find their email address

    Args:
        mattermost_handle: Mattermost username
        max_results: Maximum number of issues to return per category

    Returns:
        Dictionary with 'active' and 'completed' lists of issue dictionaries
    """
    # Get email from LDAP
    email = get_email_from_mattermost_handle(mattermost_handle)
    if not email:
        logger.warning(
            f"Could not find email for Mattermost handle {mattermost_handle}"
        )
        return {"active": [], "completed": []}

    return get_jira_issues_for_user(email, max_results)


def get_jira_issues_for_github_team_members(
    github_usernames: List[str], max_results: int = 50
) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """
    Get Jira issues for multiple GitHub team members
    Maps GitHub usernames to emails via LDAP GitHubID attribute and fetches their Jira issues

    Args:
        github_usernames: List of GitHub usernames
        max_results: Maximum number of issues per user per category

    Returns:
        Dictionary mapping GitHub username to dict with 'active' and 'completed' lists
    """
    result = {}

    for github_username in github_usernames:
        # Get email from LDAP using GitHubID attribute
        email = get_email_from_github_username(github_username)
        if not email:
            logger.warning(
                f"Could not find email for GitHub username {github_username}"
            )
            continue

        # Get Jira issues using the email directly
        issues = get_jira_issues_for_user(email, max_results)
        if (
            issues["active"] or issues["completed"]
        ):  # Only include if user has any issues
            result[github_username] = issues

    return result
