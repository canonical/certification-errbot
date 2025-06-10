import ldap3
import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

LDAP_SERVER = os.environ.get("LDAP_SERVER")
LDAP_BASE_DN = os.environ.get("LDAP_BASE_DN")
LDAP_BIND_DN = os.environ.get("LDAP_BIND_DN")
LDAP_BIND_PASSWORD = os.environ.get("LDAP_BIND_PASSWORD")

# Cache for LDAP lookups
_ldap_cache = {}

def get_github_username_from_mattermost_handle(handle: str) -> Optional[str]:
    """
    Get GitHub username from Mattermost handle using LDAP lookup
    Results are cached to avoid duplicate requests
    """
    if not all([LDAP_SERVER, LDAP_BASE_DN, LDAP_BIND_DN, LDAP_BIND_PASSWORD]):
        logger.warning("LDAP configuration incomplete")
        return None
    
    # Check cache first
    if handle in _ldap_cache:
        return _ldap_cache[handle]
    
    try:
        # Connect to LDAP server
        server = ldap3.Server(LDAP_SERVER, use_ssl=True)
        conn = ldap3.Connection(server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True)
        
        # Search for user by Mattermost handle - try multiple possible attributes
        search_filters = [
            f"(mozillaNickname={handle})",
            f"(mail={handle})",
            f"(gitHubID={handle})",
        ]
        
        for search_filter in search_filters:
            logger.debug(f"Trying search filter: {search_filter}")
            conn.search(
                search_base=LDAP_BASE_DN,
                search_filter=search_filter,
                attributes=['*']  # Get all attributes to see what's available
            )
            
            logger.debug(f"Search returned {len(conn.entries)} entries")
            
            if conn.entries:
                entry = conn.entries[0]
                logger.debug(f"Entry DN: {entry.entry_dn}")
                logger.debug(f"Available attribute keys: {list(entry.entry_attributes_as_dict.keys())}")
                
                # Log all attribute values for debugging
                # for attr_name, attr_values in entry.entry_attributes_as_dict.items():
                #     logger.debug(f"  {attr_name}: {attr_values}")
                
                github_username = entry.gitHubID.value if hasattr(entry, 'gitHubID') else None
                
                if github_username:
                    # Cache the result
                    _ldap_cache[handle] = github_username
                    logger.info(f"Found GitHub username {github_username} for Mattermost handle {handle}")
                    return github_username
                else:
                    logger.debug("No githubUsername attribute found in this entry")
                break
        
        # Cache negative result
        _ldap_cache[handle] = None
        logger.info(f"No GitHub username found for Mattermost handle {handle}")
        return None
        
    except Exception as e:
        logger.error(f"LDAP lookup failed for {handle}: {str(e)}")
        # Cache negative result to avoid repeated failed lookups
        _ldap_cache[handle] = None
        return None
    finally:
        if 'conn' in locals():
            conn.unbind()

def get_email_from_mattermost_handle(mattermost_handle: str) -> Optional[str]:
    """
    Get email address from Mattermost handle using LDAP lookup
    """
    if not all([LDAP_SERVER, LDAP_BASE_DN, LDAP_BIND_DN, LDAP_BIND_PASSWORD]):
        logger.warning("LDAP configuration incomplete")
        return None
    
    try:
        # Connect to LDAP server
        server = ldap3.Server(LDAP_SERVER, port=636, use_ssl=True)
        conn = ldap3.Connection(server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True)
        
        # Search for user by Mattermost handle - try multiple possible attributes
        search_filters = [
            f"(mozillaNickname={mattermost_handle})",
            f"(mail={mattermost_handle})",
            f"(gitHubID={mattermost_handle})",
        ]
        
        for search_filter in search_filters:
            conn.search(
                search_base=LDAP_BASE_DN,
                search_filter=search_filter,
                attributes=['mail']
            )
            
            if conn.entries:
                entry = conn.entries[0]
                logger.debug(entry)
                email = entry.mail.value if hasattr(entry, 'mail') else None
                return email
        
        return None
        
    except Exception as e:
        logger.error(f"LDAP email lookup failed for {mattermost_handle}: {str(e)}")
        return None
    finally:
        if 'conn' in locals():
            conn.unbind()
