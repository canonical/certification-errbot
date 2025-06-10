import os
import logging
from typing import List, Optional, Dict, Any
from jira import JIRA
from jira.exceptions import JIRAError

from ldap import get_email_from_mattermost_handle

logger = logging.getLogger(__name__)

JIRA_SERVER = os.environ.get("JIRA_SERVER")
JIRA_TOKEN = os.environ.get("JIRA_TOKEN")

# Cache for Jira connections
_jira_client = None


def get_jira_client() -> Optional[JIRA]:
    """Get authenticated Jira client instance"""
    global _jira_client
    
    if not all([JIRA_SERVER, JIRA_TOKEN]):
        logger.warning("Jira configuration incomplete - missing JIRA_SERVER or JIRA_TOKEN")
        return None
    
    if _jira_client is None:
        try:
            _jira_client = JIRA(
                server=JIRA_SERVER,
                token_auth=JIRA_TOKEN
            )
            logger.info("Jira client initialized successfully")
        except JIRAError as e:
            logger.error(f"Failed to initialize Jira client: {str(e)}")
            return None
    
    return _jira_client


def get_jira_issues_for_user(email: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """
    Get Jira issues assigned to a user by email address
    
    Args:
        email: User's email address
        max_results: Maximum number of issues to return
        
    Returns:
        List of issue dictionaries with key, summary, status, priority
    """
    client = get_jira_client()
    if not client:
        return []
    
    try:
        # Search for issues assigned to the user
        jql = f'assignee = "{email}" AND resolution = Unresolved ORDER BY priority DESC, updated DESC'
        
        issues = client.search_issues(
            jql_str=jql,
            maxResults=max_results,
            fields='key,summary,status,priority,assignee'
        )
        
        result = []
        for issue in issues:
            result.append({
                'key': issue.key,
                'summary': issue.fields.summary,
                'status': issue.fields.status.name,
                'priority': issue.fields.priority.name if issue.fields.priority else 'None',
                'url': f"{JIRA_SERVER}/browse/{issue.key}"
            })
        
        logger.info(f"Found {len(result)} Jira issues for {email}")
        return result
        
    except JIRAError as e:
        logger.error(f"Failed to fetch Jira issues for {email}: {str(e)}")
        return []


def get_jira_issues_for_mattermost_handle(mattermost_handle: str, max_results: int = 50) -> List[Dict[str, Any]]:
    """
    Get Jira issues for a user by their Mattermost handle
    Uses LDAP lookup to find their email address
    
    Args:
        mattermost_handle: Mattermost username
        max_results: Maximum number of issues to return
        
    Returns:
        List of issue dictionaries with key, summary, status, priority
    """
    # Get email from LDAP
    email = get_email_from_mattermost_handle(mattermost_handle)
    if not email:
        logger.warning(f"Could not find email for Mattermost handle {mattermost_handle}")
        return []
    
    return get_jira_issues_for_user(email, max_results)


def get_jira_issues_for_github_team_members(github_usernames: List[str], max_results: int = 50) -> Dict[str, List[Dict[str, Any]]]:
    """
    Get Jira issues for multiple GitHub team members
    Maps GitHub usernames to emails via LDAP and fetches their Jira issues
    
    Args:
        github_usernames: List of GitHub usernames
        max_results: Maximum number of issues per user
        
    Returns:
        Dictionary mapping GitHub username to list of their Jira issues
    """
    result = {}
    
    for github_username in github_usernames:
        # For now, assume GitHub username equals Mattermost handle
        # This could be enhanced with a reverse lookup if needed
        issues = get_jira_issues_for_mattermost_handle(github_username, max_results)
        if issues:
            result[github_username] = issues
    
    return result