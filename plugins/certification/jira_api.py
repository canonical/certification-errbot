import os
import logging
from typing import List, Optional, Dict, Any
from jira import JIRA
from jira.exceptions import JIRAError

from ldap import get_email_from_mattermost_handle, get_email_from_github_username

logger = logging.getLogger(__name__)

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
            logger.info("Jira client initialized successfully")
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
            
        logger.info("=== JIRA FIELD ANALYSIS FOR STORY POINTS ===")
        
        for issue in issues:
            logger.info(f"\nAnalyzing issue: {issue.key} - {issue.fields.summary}")
            
            # Check all custom fields
            story_point_candidates = []
            for field_name in dir(issue.fields):
                if field_name.startswith('customfield_'):
                    field_value = getattr(issue.fields, field_name, None)
                    if field_value is not None:
                        if isinstance(field_value, (int, float)):
                            story_point_candidates.append((field_name, field_value, "numeric"))
                            logger.info(f"  {field_name}: {field_value} (NUMERIC - potential story points)")
                        elif hasattr(field_value, 'value') and isinstance(field_value.value, (int, float)):
                            story_point_candidates.append((field_name, field_value.value, "object.value"))
                            logger.info(f"  {field_name}.value: {field_value.value} (OBJECT.VALUE - potential story points)")
                        elif str(field_value).replace('.', '').isdigit():
                            story_point_candidates.append((field_name, field_value, "string_numeric"))
                            logger.info(f"  {field_name}: {field_value} (STRING NUMERIC - potential story points)")
            
            if story_point_candidates:
                logger.info(f"Story point candidates for {issue.key}: {story_point_candidates}")
            else:
                logger.info(f"No story point candidates found for {issue.key}")
                
        logger.info("=== END FIELD ANALYSIS ===")
        
    except Exception as e:
        logger.error(f"Error during field identification: {str(e)}")


def refresh_jira_issues_cache():
    """
    Refresh the Jira issues cache by fetching all issues from the saved filter
    Similar to GitHub cache pattern - called from the main plugin when needed
    """
    if not JIRA_FILTER_ID:
        logger.info("JIRA_FILTER_ID not set, cannot refresh cache")
        return

    client = get_jira_client()
    if not client:
        logger.error("Failed to get Jira client for cache refresh")
        return

    try:
        logger.info(f"Refreshing Jira issues cache using filter {JIRA_FILTER_ID}")

        # Get the saved filter
        saved_filter = client.filter(JIRA_FILTER_ID)
        logger.info(f"Using saved filter: {saved_filter.name}")

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
            logger.info("Filtering issues to current sprint only")
        else:
            jql = base_jql

        logger.debug(f"Final JQL query: {jql}")

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
            logger.info(
                f"Fetched {len(issues)} issues (total so far: {len(all_issues)})"
            )
            
            # Log custom fields from the first issue to help identify story points field
            if start_at == 0 and issues:
                first_issue = issues[0]
                logger.info(f"Analyzing custom fields for issue {first_issue.key}")
                
                # Log all custom fields that might contain story points
                custom_fields = {}
                for field_name in dir(first_issue.fields):
                    if field_name.startswith('customfield_'):
                        field_value = getattr(first_issue.fields, field_name, None)
                        custom_fields[field_name] = field_value
                        # Log numeric fields that might be story points
                        if isinstance(field_value, (int, float)) and field_value > 0:
                            logger.info(f"  {field_name}: {field_value} (numeric - potential story points)")
                        elif field_value is not None:
                            logger.info(f"  {field_name}: {field_value} (type: {type(field_value)})")
                
                logger.info(f"Total custom fields found: {len(custom_fields)}")
                
                # Also log standard fields that might contain story points
                standard_fields = ['timeestimate', 'timeoriginalestimate', 'aggregatetimeestimate']
                for field_name in standard_fields:
                    if hasattr(first_issue.fields, field_name):
                        field_value = getattr(first_issue.fields, field_name)
                        if field_value:
                            logger.info(f"Standard field {field_name}: {field_value}")

            # If we got fewer results than requested, we're done
            if len(issues) < max_results:
                break

            start_at += max_results

        logger.info(f"Finished fetching all issues. Total: {len(all_issues)} issues")

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

                # Get story points (customfield_10016 is typically story points in Jira Cloud)
                story_points = getattr(issue.fields, "customfield_10016", None)
                logger.debug(f"Issue {issue.key}: story_points from customfield_10016 = {story_points} (type: {type(story_points)})")

                # Determine if issue is completed based on status category
                status_category = getattr(issue.fields.status, "statusCategory", None)
                is_completed = (
                    status_category and status_category.name.lower() == "done"
                )

                jira_issues_cache[email].append(
                    {
                        "key": issue.key,
                        "summary": issue.fields.summary,
                        "status": issue.fields.status.name,
                        "priority": issue.fields.priority.name
                        if issue.fields.priority
                        else "None",
                        "story_points": story_points,
                        "is_completed": is_completed,
                        "url": f"{JIRA_SERVER}/browse/{issue.key}",
                    }
                )

        # Log assignee emails for debugging
        assignee_emails = list(jira_issues_cache.keys())
        logger.info(
            f"Cache refreshed with {len(all_issues)} issues for {len(jira_issues_cache)} assignees: {assignee_emails}"
        )

    except JIRAError as e:
        logger.error(f"Failed to refresh issues cache: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error refreshing cache: {str(e)}")


def get_jira_issues_for_user(
    email: str, max_results: int = 50
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get Jira issues assigned to a user by email address from cache
    Separates active and completed issues

    Args:
        email: User's email address (account ID)
        max_results: Maximum number of issues to return per category

    Returns:
        Dictionary with 'active' and 'completed' lists of issue dictionaries
    """
    if email in jira_issues_cache:
        cached_issues = jira_issues_cache[email]

        # Separate active and completed issues
        active_issues = [
            issue for issue in cached_issues if not issue.get("is_completed", False)
        ]
        completed_issues = [
            issue for issue in cached_issues if issue.get("is_completed", False)
        ]

        # Sort by priority and limit results
        active_sorted = sorted(
            active_issues, key=lambda x: x.get("priority", "None"), reverse=True
        )[:max_results]
        completed_sorted = sorted(
            completed_issues, key=lambda x: x.get("priority", "None"), reverse=True
        )[:max_results]

        result = {"active": active_sorted, "completed": completed_sorted}

        logger.info(
            f"Found {len(active_sorted)} active and {len(completed_sorted)} completed Jira issues for {email}"
        )
        return result

    logger.info(f"No cached issues found for {email}")
    return {"active": [], "completed": []}


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
