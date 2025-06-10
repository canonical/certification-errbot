import requests
from os import environ
from typing import TypedDict, Any, Dict

mattermost_token = environ.get("ERRBOT_TOKEN")
mattermost_base_url = f"https://{environ.get('ERRBOT_SERVER')}/api/v4"

class UserDetails(TypedDict):
    id: str
    create_at: int
    update_at: int
    delete_at: int
    username: str
    auth_data: str
    auth_service: str
    email: str
    nickname: str
    first_name: str
    last_name: str
    position: str
    roles: str
    props: Dict[str, Any]
    last_picture_update: int
    locale: str
    timezone: Dict[str, str]
    disable_welcome_email: bool

def get_user_by_email(token, base_url, email) -> UserDetails:
    url = f"{base_url}/users/email/{email}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_user_by_name(token, base_url, user_name) -> UserDetails:
    url = f"{base_url}/users/username/{user_name}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_user_by_mattermost_id(token, base_url, user_id) -> UserDetails:
    url = f"{base_url}/plugins/github/user?mattermost_user_id={user_id}"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_mattermost_handle_by_email(token, base_url, email) -> str:
    """
    Get Mattermost handle (username) by email address
    Returns the username if found, None if not found
    """
    try:
        user_details = get_user_by_email(token, base_url, email)
        return user_details.get('username')
    except Exception:
        return None