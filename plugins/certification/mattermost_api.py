from os import environ
from typing import Any, Dict, TypedDict

import requests

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
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
