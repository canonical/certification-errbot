"""
PR formatting utilities
"""

from typing import Any, Dict, List


def format_pr_link(pr: Dict[str, Any], github_org: str) -> str:
    """Format a single PR as a markdown link."""
    repo_name = pr.get("repository", "unknown")
    pr_number = pr.get("number", "unknown")
    html_url = pr.get("html_url", "")
    return f"[{github_org}/{repo_name} #{pr_number}]({html_url})"


def _format_pr_section(
    title: str,
    prs: List[Dict[str, Any]],
    github_org: str,
    show_roles: bool = False
) -> str:
    """Format a section of PRs with a title."""
    if not prs:
        return ""
    
    lines = [f"**{title}:**"]
    for pr in prs:
        pr_link = format_pr_link(pr, github_org)
        pr_title = pr["title"]
        
        if show_roles and "user_role" in pr:
            roles = ", ".join(pr["user_role"])
            lines.append(f"- {pr_link}: {pr_title} ({roles})")
        else:
            lines.append(f"- {pr_link}: {pr_title}")
    
    return "\n".join(lines)


def _count_unique_repos(pr_data: Dict[str, List]) -> int:
    """Count unique repositories across all PR categories."""
    repos = set()
    for prs in pr_data.values():
        for pr in prs:
            if "repository" in pr:
                repos.add(pr["repository"])
    return len(repos)


def format_pr_summary(
    github_username: str,
    pr_data: Dict[str, List],
    github_org: str,
    is_digest: bool = False
) -> str:
    """
    Format PR summary for a user.
    
    Args:
        github_username: GitHub username
        pr_data: Dictionary with PR categories as keys
        github_org: GitHub organization name
        is_digest: Whether this is for a digest (different formatting)
    
    Returns:
        Formatted PR summary string
    """
    # Extract PR categories
    assigned_prs = pr_data.get("assigned", [])
    authored_unassigned = pr_data.get("authored_unassigned", [])
    authored_approved = pr_data.get("authored_approved", [])
    authored_changes_requested = pr_data.get("authored_changes_requested", [])
    authored_pending_review = pr_data.get("authored_pending_review", [])
    authored_unknown_status = pr_data.get("authored_unknown_status", [])
    
    # Count repos
    unique_repos = _count_unique_repos(pr_data)
    
    has_any_prs = any([
        assigned_prs,
        authored_unassigned,
        authored_approved,
        authored_changes_requested,
        authored_pending_review,
        authored_unknown_status
    ])
    
    if not has_any_prs:
        return _format_no_prs_message(github_username, unique_repos, github_org)
    
    # Build the summary
    sections = []
    
    # Add sections for different PR categories
    if assigned_prs:
        section = _format_pr_section(
            "PRs pending your review",
            assigned_prs,
            github_org,
            show_roles=True
        )
        sections.append(section)
    
    if authored_unassigned:
        section = _format_pr_section(
            "PRs you authored (unassigned)",
            authored_unassigned,
            github_org
        )
        sections.append(section)
    
    if authored_approved:
        section = _format_pr_section(
            "PRs you authored (approved, ready to merge)",
            authored_approved,
            github_org
        )
        sections.append(section)
    
    if authored_changes_requested:
        section = _format_pr_section(
            "PRs you authored (changes requested)",
            authored_changes_requested,
            github_org
        )
        sections.append(section)
    
    if authored_pending_review:
        section = _format_pr_section(
            "PRs you authored (pending review)",
            authored_pending_review,
            github_org
        )
        sections.append(section)
    
    if authored_unknown_status:
        section = _format_pr_section(
            "PRs you authored (review status unknown)",
            authored_unknown_status,
            github_org
        )
        sections.append(section)
    
    return "\n\n".join(sections)


def _format_no_prs_message(
    github_username: str,
    unique_repos: int,
    github_org: str
) -> str:
    """Format message when user has no PRs."""
    return (
        f"No PRs with @{github_username} as requested reviewer or assignee, "
        f"and no unassigned, approved, or changes requested PRs authored by "
        f"@{github_username} across {unique_repos} repositories in {github_org}."
    )