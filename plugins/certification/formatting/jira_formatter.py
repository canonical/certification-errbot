"""
Jira issue formatting utilities
"""

from typing import Dict, List, Any, Optional


def format_story_points(points: Optional[int]) -> str:
    """Format story points for display."""
    if not points:
        return ""
    elif points == 1:
        return " (1 story point)"
    else:
        return f" ({points} story points)"


def _format_issue_line(issue: Dict[str, Any]) -> str:
    """Format a single Jira issue as a markdown line."""
    return f"- [{issue['key']}]({issue['url']}): {issue['summary']}"


def _format_issue_section(
    title: str,
    issues: List[Dict[str, Any]],
    total_points: int
) -> str:
    """Format a section of Jira issues with title and story points."""
    if not issues:
        return ""
    
    lines = []
    
    # Add section title with story points if available
    if total_points:
        lines.append(f"**{title}{format_story_points(total_points)}:**")
    else:
        lines.append(f"**{title}:**")
    
    # Add each issue
    for issue in issues:
        lines.append(_format_issue_line(issue))
    
    return "\n".join(lines)


def format_jira_summary(
    username: str,
    jira_data: Dict[str, List],
    show_completed: bool = True
) -> str:
    """
    Format Jira issue summary for a user.
    
    Args:
        username: Username (Mattermost handle)
        jira_data: Dictionary with issue categories as keys
        show_completed: Whether to show completed issues
    
    Returns:
        Formatted Jira summary string
    """
    active_issues = jira_data.get("active", [])
    review_issues = jira_data.get("review", [])
    completed_issues = jira_data.get("completed", []) if show_completed else []
    untriaged_issues = jira_data.get("untriaged", [])
    
    # Check if there are any issues
    has_any_issues = any([active_issues, review_issues, completed_issues, untriaged_issues])
    
    if not has_any_issues:
        return f"No Jira issues assigned to @{username}"
    
    # Calculate total story points
    def sum_points(issues):
        return sum(issue.get("story_points", 0) for issue in issues)
    
    active_points = sum_points(active_issues)
    review_points = sum_points(review_issues)
    completed_points = sum_points(completed_issues)
    
    # Build the summary
    sections = [f"Jira issues assigned to @{username}:"]
    
    # Add sections for different issue categories
    if active_issues:
        section = _format_issue_section("Active", active_issues, active_points)
        sections.append(section)
    
    if review_issues:
        section = _format_issue_section("In Review", review_issues, review_points)
        sections.append(section)
    
    if completed_issues:
        section = _format_issue_section(
            "Completed during the pulse",
            completed_issues,
            completed_points
        )
        sections.append(section)
    
    if untriaged_issues:
        section = _format_issue_section("Untriaged", untriaged_issues, 0)
        sections.append(section)
    
    # Add total summary
    total_points = active_points + review_points + completed_points
    if total_points > 0:
        sections.append(f"\n**Total{format_story_points(total_points)}**")
    
    return "\n\n".join(sections)


def format_team_jira_summary(
    team_name: str,
    team_data: Dict[str, Dict[str, List]],
    user_handles: Dict[str, str]
) -> str:
    """
    Format Jira summary for a team.
    
    Args:
        team_name: GitHub team name
        team_data: Dictionary mapping usernames to their Jira data
        user_handles: Dictionary mapping GitHub usernames to Mattermost handles
    
    Returns:
        Formatted team Jira summary
    """
    if not team_data:
        return f"No Jira issues found for team {team_name}"
    
    sections = [f"Jira issues assigned to team {team_name}:"]
    
    # Process each team member
    for github_username, jira_data in team_data.items():
        # Get Mattermost handle
        mattermost_handle = user_handles.get(github_username, github_username)
        
        # Check if user has any issues
        has_issues = any([
            jira_data.get("active", []),
            jira_data.get("review", []),
            jira_data.get("completed", []),
            jira_data.get("untriaged", [])
        ])
        
        if has_issues:
            # Format user's issues (without completed by default for team view)
            user_summary = format_jira_summary(
                mattermost_handle,
                jira_data,
                show_completed=False  # Don't show completed in team view
            )
            # Remove the "No Jira issues" prefix if present
            if not user_summary.startswith("No Jira"):
                sections.append(user_summary)
    
    return "\n\n".join(sections)