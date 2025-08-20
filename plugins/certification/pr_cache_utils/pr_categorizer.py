"""
PR categorization logic extracted from PullRequestCache.get_prs_for_user
"""

from typing import Dict, List, Optional, Tuple


def categorize_pr_for_user(
    pr: dict,
    repo_name: str,
    github_username: str,
    review_status_fetcher=None
) -> Tuple[str, dict]:
    """
    Categorize a PR for a specific user.
    
    Args:
        pr: Pull request data
        repo_name: Repository name
        github_username: GitHub username to check
        review_status_fetcher: Callable to fetch review status (repo_name, pr_number) -> Optional[Dict]
    
    Returns:
        Tuple of (category_name, pr_with_metadata) or (None, None) if not relevant
    """
    requested_reviewers = pr.get("requested_reviewers", [])
    assignees = pr.get("assignees", [])
    author = pr.get("user", {}).get("login", "")
    
    # Check if user is assigned as reviewer or assignee
    is_requested_reviewer = _is_user_in_list(github_username, requested_reviewers)
    is_assignee = _is_user_in_list(github_username, assignees)
    
    if is_requested_reviewer or is_assignee:
        pr_with_repo = _add_pr_metadata(pr, repo_name)
        pr_with_repo["user_role"] = _get_user_roles(is_requested_reviewer, is_assignee)
        return ("assigned", pr_with_repo)
    
    # Check if PR is authored by user
    if author.lower() == github_username.lower():
        pr_with_repo = _add_pr_metadata(pr, repo_name)
        return _categorize_authored_pr(pr, pr_with_repo, review_status_fetcher, repo_name)
    
    return (None, None)


def _is_user_in_list(username: str, user_list: List[dict]) -> bool:
    """Check if username is in a list of user objects."""
    return any(
        user["login"].lower() == username.lower()
        for user in user_list
    )


def _add_pr_metadata(pr: dict, repo_name: str) -> dict:
    """Add repository metadata to PR."""
    pr_with_repo = pr.copy()
    pr_with_repo["repository"] = repo_name
    return pr_with_repo


def _get_user_roles(is_reviewer: bool, is_assignee: bool) -> List[str]:
    """Get list of user roles for a PR."""
    roles = []
    if is_reviewer:
        roles.append("reviewer")
    if is_assignee:
        roles.append("assignee")
    return roles


def _categorize_authored_pr(
    pr: dict,
    pr_with_repo: dict,
    review_status_fetcher,
    repo_name: str
) -> Tuple[str, dict]:
    """
    Categorize a PR authored by the user.
    
    Returns:
        Tuple of (category_name, pr_data)
    """
    requested_reviewers = pr.get("requested_reviewers", [])
    requested_teams = pr.get("requested_teams", [])
    assignees = pr.get("assignees", [])
    
    # Check if it has no reviewers, teams, or assignees
    if not any([requested_reviewers, requested_teams, assignees]):
        return ("authored_unassigned", pr_with_repo)
    
    # Check review status if fetcher is provided
    if review_status_fetcher:
        review_status = review_status_fetcher(repo_name, pr["number"])
        
        if review_status is None:
            # Error fetching review status
            return ("authored_unknown_status", pr_with_repo)
        elif review_status.get("has_changes_requested"):
            return ("authored_changes_requested", pr_with_repo)
        elif review_status.get("has_approvals"):
            return ("authored_approved", pr_with_repo)
        else:
            # Has reviewers/assignees but no review activity yet
            return ("authored_pending_review", pr_with_repo)
    
    # No review status fetcher provided, treat as pending
    return ("authored_pending_review", pr_with_repo)