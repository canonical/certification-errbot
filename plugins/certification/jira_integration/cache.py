"""
Jira issues cache management
"""

import logging
import os
from typing import Any, Dict, List, Optional

from jira.exceptions import JIRAError

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ldap import get_email_from_github_username, get_email_from_mattermost_handle
from .client import JIRA_FILTER_ID, JIRA_SERVER, get_jira_client
from .priority import get_priority_sort_key, is_review_status

logger = logging.getLogger(__name__)

# Cache for Jira issues by user email
jira_issues_cache: Dict[str, List[Dict[str, Any]]] = {}

# Mapping of Jira account IDs to emails
jira_account_to_email: Dict[str, str] = {}


def _build_jql_query(base_jql: str, sprint_filter: bool) -> str:
    """
    Build JQL query with optional sprint filtering

    Args:
        base_jql: Base JQL from saved filter
        sprint_filter: Whether to filter by current sprint

    Returns:
        Modified JQL query string
    """
    if not sprint_filter:
        return base_jql

    # Handle ORDER BY clause properly when adding sprint filter
    if "ORDER BY" in base_jql.upper():
        jql_parts = base_jql.split("ORDER BY")
        return (
            f"{jql_parts[0].strip()} AND sprint in openSprints() "
            f"ORDER BY {jql_parts[1].strip()}"
        )
    else:
        return f"{base_jql} AND sprint in openSprints()"


def _fetch_all_issues(client, jql: str, max_results: int = 100):
    """
    Fetch all issues from Jira with pagination

    Args:
        client: JIRA client instance
        jql: JQL query string
        max_results: Page size for pagination

    Returns:
        List of all fetched issues
    """
    all_issues = []
    start_at = 0

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

    return all_issues


def _extract_issue_data(issue, jira_server: str) -> Dict[str, Any]:
    """
    Extract relevant data from a Jira issue

    Args:
        issue: JIRA issue object
        jira_server: JIRA server URL for building links

    Returns:
        Dictionary with extracted issue data
    """
    # Get story points (customfield_10024 per user requirements)
    story_points = getattr(issue.fields, "customfield_10024", None)

    # Determine issue state based on status
    status_name = issue.fields.status.name
    status_category = getattr(issue.fields.status, "statusCategory", None)
    is_completed = status_category and status_category.name.lower() == "done"
    is_in_review = is_review_status(status_name)

    # Get priority safely
    priority = "None"
    if issue.fields.priority:
        priority = issue.fields.priority.name

    return {
        "key": issue.key,
        "summary": issue.fields.summary,
        "status": status_name,
        "priority": priority,
        "story_points": story_points,
        "is_completed": is_completed,
        "is_in_review": is_in_review,
        "url": f"{jira_server}/browse/{issue.key}",
    }


def _process_issue_assignee(issue, jira_issues_cache, jira_account_to_email):
    """
    Process assignee information from an issue and update caches

    Args:
        issue: JIRA issue object
        jira_issues_cache: Cache dictionary to update
        jira_account_to_email: Account mapping dictionary to update

    Returns:
        Email address of assignee or None
    """
    if not (hasattr(issue.fields, "assignee") and issue.fields.assignee):
        return None

    account_id = issue.fields.assignee.accountId
    email = getattr(issue.fields.assignee, "emailAddress", account_id)

    # Store account ID to email mapping
    jira_account_to_email[account_id] = email

    # Initialize cache entry if needed
    if email not in jira_issues_cache:
        jira_issues_cache[email] = []

    return email


def refresh_jira_issues_cache():
    """
    Refresh the Jira issues cache by fetching all issues from the saved filter
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

        # Build JQL query with optional sprint filtering
        sprint_filter = (
            os.environ.get("JIRA_CURRENT_SPRINT_ONLY", "false").lower() == "true"
        )
        jql = _build_jql_query(saved_filter.jql, sprint_filter)

        # Fetch all issues
        all_issues = _fetch_all_issues(client, jql)

        # Clear and rebuild the cache
        jira_issues_cache.clear()
        jira_account_to_email.clear()

        # Process each issue
        for issue in all_issues:
            email = _process_issue_assignee(issue, jira_issues_cache, jira_account_to_email)
            if email:
                issue_data = _extract_issue_data(issue, JIRA_SERVER)
                jira_issues_cache[email].append(issue_data)

        # Log summary
        logger.info(
            f"Refreshed Jira cache: {len(all_issues)} issues for "
            f"{len(jira_issues_cache)} users"
        )

    except JIRAError as e:
        logger.error(f"Failed to refresh issues cache: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error refreshing cache: {str(e)}")


def _categorize_issues(cached_issues: List[Dict[str, Any]]) -> Dict[str, List]:
    """
    Categorize issues by their state and priority

    Args:
        cached_issues: List of cached issue dictionaries

    Returns:
        Dictionary with categorized issues
    """
    # Separate issues by state and priority
    untriaged_issues = [
        issue
        for issue in cached_issues
        if not issue.get("is_completed", False)
        and (
            not issue.get("priority")
            or issue.get("priority", "").lower() in ["none", ""]
        )
    ]

    active_issues = [
        issue
        for issue in cached_issues
        if not issue.get("is_completed", False)
        and not issue.get("is_in_review", False)
        and issue.get("priority")
        and issue.get("priority", "").lower() not in ["none", ""]
    ]

    review_issues = [
        issue
        for issue in cached_issues
        if not issue.get("is_completed", False)
        and issue.get("is_in_review", False)
        and issue.get("priority")
        and issue.get("priority", "").lower() not in ["none", ""]
    ]

    completed_issues = [
        issue for issue in cached_issues if issue.get("is_completed", False)
    ]

    return {
        "untriaged": untriaged_issues,
        "active": active_issues,
        "review": review_issues,
        "completed": completed_issues,
    }


def get_jira_issues_for_user(
    email: str, max_results: int = 50
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get Jira issues assigned to a user by email address from cache

    Args:
        email: User's email address (account ID)
        max_results: Maximum number of issues to return per category

    Returns:
        Dictionary with 'active', 'review', 'completed', and 'untriaged' lists
    """
    if email not in jira_issues_cache:
        return {"active": [], "review": [], "completed": [], "untriaged": []}

    cached_issues = jira_issues_cache[email]
    categorized = _categorize_issues(cached_issues)

    # Sort by priority and limit results
    result = {}
    for category in ["active", "review", "completed"]:
        sorted_issues = sorted(
            categorized[category],
            key=lambda x: get_priority_sort_key(x.get("priority", "")),
        )[:max_results]
        result[category] = sorted_issues

    # Untriaged issues don't need priority sorting (they have no priority)
    result["untriaged"] = categorized["untriaged"][:max_results]

    return result


def get_jira_issues_for_mattermost_handle(
    mattermost_handle: str,
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get Jira issues for a Mattermost user (maps handle to email via LDAP)

    Args:
        mattermost_handle: Mattermost username

    Returns:
        Dictionary with issue lists or empty structure if user not found
    """
    email = get_email_from_mattermost_handle(mattermost_handle)
    if not email:
        logger.warning(f"Could not find email for Mattermost handle {mattermost_handle}")
        return {"active": [], "completed": []}

    return get_jira_issues_for_user(email, max_results=50)


def get_jira_issues_for_github_team_members(
    github_usernames: List[str], max_results: int = 50
) -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
    """
    Get Jira issues for multiple GitHub team members

    Args:
        github_usernames: List of GitHub usernames
        max_results: Maximum results per user per category

    Returns:
        Dictionary mapping GitHub username to their issues
    """
    team_issues = {}

    for github_username in github_usernames:
        email = get_email_from_github_username(github_username)
        if email:
            issues = get_jira_issues_for_user(email, max_results)
            # Only include users with actual issues
            if any(
                issues[cat]
                for cat in ["active", "review", "completed", "untriaged"]
                if cat in issues
            ):
                team_issues[github_username] = issues

    return team_issues