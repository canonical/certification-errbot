import requests

github_email_cache: dict[str, str] = {}


def get_github_username_from_email(github_token, email):
    """
    Get GitHub username from email address using GitHub API
    Results are cached to avoid duplicate requests
    """
    if not github_token:
        return None

    # Check cache first
    if email in github_email_cache:
        return github_email_cache[email]

    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        # Search for users by email
        search_url = f"https://api.github.com/search/users?q={email}+in:email"
        response = requests.get(search_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data.get("total_count", 0) > 0:
                username = data["items"][0]["login"]
                # Cache the result
                github_email_cache[email] = username
                return username
    except requests.exceptions.RequestException:
        pass

    # Cache negative result to avoid repeated failed lookups
    github_email_cache[email] = None
    return None
