from mattermost_api import (
    get_user_by_email,
    get_user_by_name,
    mattermost_token,
    mattermost_base_url,
)
import logging

logger = logging.getLogger(__name__)

user_cache_by_email: dict[str, str] = {}
user_cache_by_username: dict[str, str | None] = {}


def get_user_handle(email: str) -> str | None:
    if email in user_cache_by_email:
        return user_cache_by_email[email]
    else:
        assignee_handle = get_user_by_email(
            mattermost_token, mattermost_base_url, email
        )
        user_cache_by_email[email] = assignee_handle
        return assignee_handle


def get_user_email(username: str) -> str | None:
    if username in user_cache_by_username:
        return user_cache_by_username[username]
    else:
        user_details = get_user_by_name(mattermost_token, mattermost_base_url, username)
        if user_details:
            email = user_details.get("email")
            if email:
                user_cache_by_username[username] = email
                return email
        user_cache_by_username[username] = None
        return None
