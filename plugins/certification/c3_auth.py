import requests


def get_access_token(base_url: str, client_id: str, client_secret: str) -> str:
    response = requests.post(
        f"{base_url}/oauth2/token/",
        auth=(client_id, client_secret),
        data={"grant_type": "client_credentials", "scope": "read write"},
    )
    if not response.ok:
        raise RuntimeError(
            f"Failed to log in to C3 via {base_url}/oauth2/token: {response.status_code} {response.text}"
        )

    return response.json()["access_token"]
