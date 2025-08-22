"""
Digest generation utilities
"""

import os
import sys
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jira_integration import get_jira_issues_for_user
from ldap import get_email_from_github_username, get_email_from_mattermost_handle

from .jira_formatter import format_jira_summary
from .pr_formatter import format_pr_summary


def generate_user_digest(
    github_username: str,
    mattermost_username: str,
    pr_data: Dict[str, List],
    github_org: str,
    use_github_for_jira: bool = False
) -> Optional[str]:
    """
    Generate a digest for a user including PRs and Jira issues.
    
    Args:
        github_username: GitHub username
        mattermost_username: Mattermost username
        pr_data: PR data from cache
        github_org: GitHub organization
        use_github_for_jira: Whether to use GitHub username for Jira lookup
    
    Returns:
        Formatted digest string or None if no content
    """
    sections = []
    
    # Add PR summary if there are PRs
    if _has_prs(pr_data):
        pr_summary = format_pr_summary(
            github_username,
            pr_data,
            github_org,
            is_digest=True
        )
        if pr_summary and not pr_summary.startswith("No PRs"):
            sections.append(pr_summary)
    
    # Add Jira summary
    jira_summary = _get_jira_summary_for_digest(
        github_username if use_github_for_jira else mattermost_username,
        use_github_for_jira
    )
    
    if jira_summary:
        sections.append(jira_summary)
    
    if sections:
        return "\n\n---\n\n".join(sections)
    return None


def _has_prs(pr_data: Dict[str, List]) -> bool:
    """Check if there are any PRs in the data."""
    return any(pr_data.get(key, []) for key in [
        "assigned",
        "authored_unassigned",
        "authored_approved",
        "authored_changes_requested",
        "authored_pending_review",
        "authored_unknown_status"
    ])


def _get_jira_summary_for_digest(
    username: str,
    use_github: bool
) -> Optional[str]:
    """Get Jira summary for digest, handling both GitHub and Mattermost usernames."""
    if use_github:
        email = get_email_from_github_username(username)
    else:
        email = get_email_from_mattermost_handle(username)
    
    if not email:
        return None
    
    jira_data = get_jira_issues_for_user(email)
    
    has_issues = any([
        jira_data.get("active", []),
        jira_data.get("review", []),
        jira_data.get("completed", [])
    ])
    
    if has_issues:
        return format_jira_summary(username, jira_data, show_completed=True, use_second_person=True)
    
    return None