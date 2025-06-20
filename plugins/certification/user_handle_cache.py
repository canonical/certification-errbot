from mattermost_api import get_user_by_email, mattermost_base_url, mattermost_token

user_cache: dict[str, str] = {}


def get_assignee_handle(email: str) -> str | None:
    if email in user_cache:
        return user_cache[email]
    else:
        assignee_handle = get_user_by_email(
            mattermost_token, mattermost_base_url, email
        )
        user_cache[email] = assignee_handle
        return assignee_handle
