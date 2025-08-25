"""
PR review status checking logic
"""

import logging
from typing import Dict, Optional

import requests

logger = logging.getLogger(__name__)


def get_pr_review_status(
    repo_name: str,
    pr_number: int,
    github_org: str,
    headers: dict
) -> Optional[Dict[str, bool]]:
    """
    Get review status for a specific PR.
    
    Args:
        repo_name: Repository name
        pr_number: PR number
        github_org: GitHub organization
        headers: GitHub API headers with authentication
    
    Returns:
        dict with 'has_approvals' and 'has_changes_requested' booleans on success,
        None if an error occurs.
    """
    try:
        url = f"https://api.github.com/repos/{github_org}/{repo_name}/pulls/{pr_number}/reviews"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            logger.warning(
                f"Failed to fetch reviews for {repo_name}#{pr_number}: "
                f"status {response.status_code}"
            )
            return None
        
        reviews = response.json()
        return _analyze_review_states(reviews)
        
    except requests.exceptions.RequestException as e:
        logger.error(
            f"Network error fetching reviews for {repo_name}#{pr_number}: {e}"
        )
        return None
    except Exception as e:
        logger.error(
            f"Unexpected error fetching reviews for {repo_name}#{pr_number}: {e}"
        )
        return None


def _analyze_review_states(reviews: list) -> Dict[str, bool]:
    """
    Analyze review states to determine approval/changes requested status.
    
    Args:
        reviews: List of review objects from GitHub API
    
    Returns:
        Dict with 'has_approvals' and 'has_changes_requested' booleans
    """
    has_approvals = False
    has_changes_requested = False
    
    for review in reviews:
        state = review.get("state")
        if state == "APPROVED":
            has_approvals = True
        elif state == "CHANGES_REQUESTED":
            has_changes_requested = True
    
    return {
        "has_approvals": has_approvals,
        "has_changes_requested": has_changes_requested
    }