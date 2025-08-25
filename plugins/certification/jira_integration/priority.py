"""
Jira priority-related utilities
"""


def get_priority_sort_key(priority: str) -> int:
    """
    Return a sort key for Jira priority ordering.
    Lower numbers = higher priority

    Args:
        priority: Jira priority name (e.g., "Highest", "High", "Medium", etc.)

    Returns:
        Sort key (1-6, where 1 is highest priority)
    """
    priority_lower = priority.lower() if priority else ""
    priority_order = {
        "highest": 1,
        "high": 2,
        "medium": 3,
        "low": 4,
        "lowest": 5,
    }
    return priority_order.get(priority_lower, 6)  # Unknown priorities get lowest priority


def is_review_status(status_name: str) -> bool:
    """
    Check if a Jira status name indicates the issue is in review

    Args:
        status_name: The name of the Jira status

    Returns:
        True if the status indicates a review state
    """
    if not status_name:
        return False

    review_keywords = [
        "review",
        "code review",
        "peer review",
        "in review",
        "awaiting review",
        "under review",
    ]

    status_lower = status_name.lower()
    return any(keyword in status_lower for keyword in review_keywords)