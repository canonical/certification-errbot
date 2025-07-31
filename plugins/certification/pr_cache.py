import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

logger = logging.getLogger(__name__)


class PullRequestCache:
    """
    Cache for GitHub Pull Requests across specified repositories in an organization.
    Periodically fetches and caches PR data to reduce API calls.
    """

    def __init__(
        self,
        repo_filter: Optional[List[str]] = None,
        github_token: str | None = None,
        github_org: str | None = None,
    ):
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN")
        self.github_org = github_org or os.environ.get("GITHUB_ORG")
        self.repo_filter = repo_filter  # If provided, only fetch PRs from these repos
        self.cache: Dict[str, List[dict]] = {}  # repo_name -> list of PRs
        self.last_updated: Optional[datetime] = None
        self.cache_expiry_minutes = 15  # Cache expires after 15 minutes

        if not self.github_token:
            raise Exception("GITHUB_TOKEN must be set")
        if not self.github_org:
            raise Exception("GITHUB_ORG must be set")

    def _get_headers(self) -> dict:
        """Get GitHub API headers with authentication"""
        return {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def _get_repositories_to_fetch(self) -> List[str]:
        """Get list of repositories to fetch PRs from"""
        if self.repo_filter:
            # Use the provided filter list
            logger.info(
                f"Using filtered repository list: {len(self.repo_filter)} repositories"
            )
            return self.repo_filter.copy()
        else:
            # Fetch all repositories from the organization
            return self._fetch_all_org_repositories()

    def _fetch_all_org_repositories(self) -> List[str]:
        """Fetch all repository names for the organization"""
        headers = self._get_headers()
        repos = []
        page = 1
        per_page = 100

        while True:
            url = f"https://api.github.com/orgs/{self.github_org}/repos"
            params = {"page": page, "per_page": per_page, "type": "all"}

            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()

                page_repos = response.json()
                if not page_repos:
                    break

                repos.extend([repo["name"] for repo in page_repos])
                page += 1

            except requests.exceptions.RequestException as e:
                logger.error(
                    f"Error fetching repositories for org {self.github_org}: {e}"
                )
                break

        logger.info(f"Found {len(repos)} repositories in {self.github_org}")
        return repos

    def _fetch_prs_for_repo(self, repo_name: str) -> Optional[List[dict]]:
        """Fetch all open PRs for a specific repository"""
        headers = self._get_headers()
        prs = []
        page = 1
        per_page = 100

        while True:
            url = f"https://api.github.com/repos/{self.github_org}/{repo_name}/pulls"
            params = {"state": "open", "page": page, "per_page": per_page}

            try:
                response = requests.get(url, headers=headers, params=params)

                # Handle 404 for repositories that don't exist or are not accessible
                if response.status_code == 404:
                    logger.warning(
                        f"Repository {self.github_org}/{repo_name} not found or not accessible"
                    )
                    return []

                response.raise_for_status()

                page_prs = response.json()
                if not page_prs:
                    break

                # Filter out draft PRs before adding to cache
                non_draft_prs = [pr for pr in page_prs if not pr.get("draft", False)]
                prs.extend(non_draft_prs)
                page += 1

            except requests.exceptions.RequestException as e:
                logger.error(
                    f"Error fetching PRs for {self.github_org}/{repo_name}: {e}"
                )
                return None

        return prs

    def refresh_cache(self) -> bool:
        """Refresh the entire PR cache with data from specified repositories"""
        try:
            filter_info = (
                f"(filtered: {len(self.repo_filter)} repos)"
                if self.repo_filter
                else "(all repos)"
            )
            logger.info(
                f"Refreshing PR cache for organization {self.github_org} {filter_info}"
            )

            # Get repositories to fetch
            repo_names = self._get_repositories_to_fetch()

            new_cache = {}
            total_prs = 0
            successful_repos = 0

            # Fetch PRs for each repository
            for repo_name in repo_names:
                prs = self._fetch_prs_for_repo(repo_name)
                if prs is not None:  # Only cache if fetch was successful
                    new_cache[repo_name] = prs
                    total_prs += len(prs)
                    successful_repos += 1
                    logger.debug(f"Cached {len(prs)} PRs for {repo_name}")
                else:
                    logger.warning(f"Failed to fetch PRs for {repo_name}, skipping")

            self.cache = new_cache
            self.last_updated = datetime.now()

            logger.info(
                f"PR cache refreshed successfully. {total_prs} PRs across {successful_repos}/{len(repo_names)} repositories"
            )
            return True

        except Exception as e:
            logger.error(f"Error refreshing PR cache: {e}")
            return False

    def is_cache_expired(self) -> bool:
        """Check if the cache has expired"""
        if self.last_updated is None:
            return True

        expiry_time = self.last_updated + timedelta(minutes=self.cache_expiry_minutes)
        return datetime.now() > expiry_time

    def get_prs_for_user(self, github_username: str) -> dict:
        """
        Get PRs relevant to a specific GitHub user.
        Returns dict with 'assigned', 'authored_unassigned', 'authored_approved', and 'authored_changes_requested' lists.
        """
        # Refresh cache if expired
        if self.is_cache_expired():
            logger.info("PR cache expired, refreshing...")
            self.refresh_cache()

        assigned_prs = []
        authored_unassigned_prs = []
        authored_approved_prs = []
        authored_changes_requested_prs = []
        authored_pending_review_prs = []

        # Search through all cached PRs
        for repo_name, prs in self.cache.items():
            for pr in prs:
                requested_reviewers = pr.get("requested_reviewers", [])
                assignees = pr.get("assignees", [])
                author = pr.get("user", {}).get("login", "")

                # Check if PR is assigned to the user for review or as assignee
                is_requested_reviewer = any(
                    reviewer["login"].lower() == github_username.lower()
                    for reviewer in requested_reviewers
                )
                is_assignee = any(
                    assignee["login"].lower() == github_username.lower()
                    for assignee in assignees
                )

                if is_requested_reviewer or is_assignee:
                    pr_with_repo = pr.copy()
                    pr_with_repo["repository"] = repo_name
                    pr_with_repo["user_role"] = []
                    if is_requested_reviewer:
                        pr_with_repo["user_role"].append("reviewer")
                    if is_assignee:
                        pr_with_repo["user_role"].append("assignee")
                    assigned_prs.append(pr_with_repo)

                # Check if PR is authored by user
                elif author.lower() == github_username.lower():
                    pr_with_repo = pr.copy()
                    pr_with_repo["repository"] = repo_name

                    # Check if it has no reviewers or assignees
                    if len(requested_reviewers) == 0 and len(assignees) == 0:
                        authored_unassigned_prs.append(pr_with_repo)
                    else:
                        # Check review status - fetch review data
                        review_status = self._get_pr_review_status(
                            repo_name, pr["number"]
                        )
                        if review_status["has_changes_requested"]:
                            authored_changes_requested_prs.append(pr_with_repo)
                        elif review_status["has_approvals"]:
                            authored_approved_prs.append(pr_with_repo)
                        else:
                            # Has reviewers/assignees but no review activity yet
                            authored_pending_review_prs.append(pr_with_repo)

        return {
            "assigned": assigned_prs,
            "authored_unassigned": authored_unassigned_prs,
            "authored_approved": authored_approved_prs,
            "authored_changes_requested": authored_changes_requested_prs,
            "authored_pending_review": authored_pending_review_prs,
        }

    def get_cache_stats(self) -> dict:
        """Get statistics about the current cache"""
        total_prs = sum(len(prs) for prs in self.cache.values())
        return {
            "last_updated": self.last_updated,
            "total_repositories": len(self.cache),
            "total_prs": total_prs,
            "cache_expired": self.is_cache_expired(),
        }

    def get_team_members(self, team_name: str) -> List[str]:
        """
        Get list of GitHub usernames for members of a specific team.
        Returns list of usernames, empty list if team not found or error occurs.
        """
        if not team_name:
            logger.warning("No team name provided")
            return []

        headers = self._get_headers()
        members = []
        page = 1
        per_page = 100

        while True:
            url = f"https://api.github.com/orgs/{self.github_org}/teams/{team_name}/members"
            params = {"page": page, "per_page": per_page}

            try:
                response = requests.get(url, headers=headers, params=params)

                # Handle 404 for teams that don't exist or are not accessible
                if response.status_code == 404:
                    logger.warning(
                        f"Team {self.github_org}/{team_name} not found or not accessible"
                    )
                    return []

                response.raise_for_status()

                page_members = response.json()
                if not page_members:
                    break

                members.extend([member["login"] for member in page_members])
                page += 1

            except requests.exceptions.RequestException as e:
                logger.error(
                    f"Error fetching team members for {self.github_org}/{team_name}: {e}"
                )
                return []

        logger.info(f"Found {len(members)} members in team {team_name}")
        return members

    def _get_pr_review_status(self, repo_name: str, pr_number: int) -> dict:
        """
        Get review status for a specific PR.
        Returns dict with 'has_approvals' and 'has_changes_requested' booleans.
        """
        headers = self._get_headers()

        try:
            url = f"https://api.github.com/repos/{self.github_org}/{repo_name}/pulls/{pr_number}/reviews"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                reviews = response.json()
                has_approvals = False
                has_changes_requested = False

                # Check review states
                for review in reviews:
                    state = review.get("state")
                    if state == "APPROVED":
                        has_approvals = True
                    elif state == "CHANGES_REQUESTED":
                        has_changes_requested = True

                return {
                    "has_approvals": has_approvals,
                    "has_changes_requested": has_changes_requested,
                }
            elif response.status_code == 404:
                logger.debug(f"PR {repo_name}#{pr_number} not found or not accessible")
            else:
                logger.warning(
                    f"Error fetching reviews for {repo_name}#{pr_number}: {response.status_code}"
                )

        except requests.exceptions.RequestException as e:
            logger.warning(f"Error fetching reviews for {repo_name}#{pr_number}: {e}")

        # Default to no approvals or changes requested if error occurs
        return {"has_approvals": False, "has_changes_requested": False}

    def _check_pr_has_approvals(self, repo_name: str, pr_number: int) -> bool:
        """
        Legacy method for backward compatibility.
        Check if a specific PR has any approved reviews.
        Returns True if PR has at least one approved review.
        """
        status = self._get_pr_review_status(repo_name, pr_number)
        return status["has_approvals"]


# Global cache instance - will be initialized with repository filter in certification.py
pr_cache = None
