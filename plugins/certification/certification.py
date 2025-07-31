import os
from datetime import datetime
import logging

from dotenv import load_dotenv
from errbot import BotPlugin, botcmd
from config import DIGEST_SEND_TIME

from c3.client import AuthenticatedClient as C3Client
from c3.api.physicalmachinesview.physicalmachinesview_list import (
    sync_detailed as get_physicalmachinesview,
)
from c3_auth import get_access_token as get_c3_access_token
from artefacts import reply_with_artefacts_summary
from ldap import (
    get_github_username_from_mattermost_handle,
    get_email_from_mattermost_handle,
    get_mattermost_handle_from_github_username,
)
from github import get_github_username_from_email
from pr_cache import PullRequestCache
from jira_api import (
    get_jira_issues_for_mattermost_handle,
    get_jira_issues_for_github_team_members,
    refresh_jira_issues_cache,
    jira_issues_cache,
)

try:
    from llm_api import get_llm_client

    LLM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"LLM functionality not available: {e}")
    LLM_AVAILABLE = False

    def get_llm_client():
        return None


from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import ssl_fix  # noqa: F401

# Load environment variables from .env file if present
load_dotenv()
logger = logging.getLogger(__name__)


c3_client_id = os.environ.get("C3_CLIENT_ID")
c3_client_secret = os.environ.get("C3_CLIENT_SECRET")

mattermost_token = os.environ.get("ERRBOT_TOKEN")
mattermost_base_url = f"https://{os.environ.get('ERRBOT_SERVER')}/api/v4"
github_token = os.environ.get("GITHUB_TOKEN")
github_org = os.environ.get("GITHUB_ORG")
github_team = os.environ.get("GITHUB_TEAM")

llm_api_server = os.environ.get("LLM_API_SERVER", "http://localhost:11434")
llm_api_token = os.environ.get("LLM_API_TOKEN")
llm_model_name = os.environ.get("LLM_MODEL_NAME", "deepseek-r1:70b")

if not c3_client_id or not c3_client_secret:
    raise Exception("C3_CLIENT_ID and C3_CLIENT_SECRET must be set")

if not github_token:
    raise Exception("GITHUB_TOKEN must be set")

if not github_org:
    raise Exception("GITHUB_ORG must be set")

C3_BASE_URL = "https://certification.canonical.com"

c3_access_token = get_c3_access_token(C3_BASE_URL, c3_client_id, c3_client_secret)

now = datetime.now().date()

# Default repositories to monitor for PRs
DEFAULT_REPOS = [
    "blueprints",
    "certification-docs",
    "certification-lab-ci",
    "certification-lab-manager",
    "certification-ops",
    "charm-weebl",
    "charm-integration-testing",
    "checkbox",
    "django-rest-generator",
    "fcbtest",
    "hardware-api",
    "hexr",
    "hwcert-jenkins-jobs",
    "hwcert-jenkins-tools",
    "kubeflow-autotriager",
    "openapi-rest-proxy",
    "project_comp",
    "sqa-cloud-deployment-pipeline",
    "test_observer",
    "test_scheduler",
    "testflinger",
    "testflinger-agent-charm-configs",
    "ubuntu-gui-testing",
    "ubuntu.com",
    "weebl",
    "weebl-tools",
    "windows-server-virtualization-certification",
    "yarf",
]

# Get repositories from environment variable or use defaults
github_repositories_env = os.environ.get("GITHUB_REPOSITORIES")
if github_repositories_env:
    GITHUB_REPOS = [
        repo.strip() for repo in github_repositories_env.split(",") if repo.strip()
    ]
else:
    GITHUB_REPOS = DEFAULT_REPOS


class CertificationPlugin(BotPlugin):
    """
    A plugin for interacting with Certification things
    """

    def __init__(self, bot, name):
        super().__init__(bot, name)
        # Initialize PR cache with configured repository filter
        self.pr_cache = PullRequestCache(repo_filter=GITHUB_REPOS)

    def activate(self):
        super().activate()

        scheduler = BackgroundScheduler()

        # Parse the digest send time from config
        try:
            hour, minute = map(int, DIGEST_SEND_TIME.split(":"))
        except ValueError:
            # Default to 6:30 if parsing fails
            hour, minute = 6, 30
            self.log.warning(f"Invalid DIGEST_SEND_TIME format: {DIGEST_SEND_TIME}, using default 6:30")

        # Daily artefact digest (Mon-Fri at configured time UTC)
        digest_trigger = CronTrigger(
            day_of_week="mon-fri", hour=hour, minute=minute, timezone="UTC"
        )
        scheduler.add_job(self.polled_digest_sending, digest_trigger)
        self.log.info(f"Scheduled daily digest for {hour:02d}:{minute:02d} UTC")

        # PR cache refresh (every 5 minutes)
        pr_cache_trigger = CronTrigger(minute="*/5", timezone="UTC")
        scheduler.add_job(self.refresh_pr_cache, pr_cache_trigger)

        # Jira issues cache refresh (every 15 minutes)
        jira_cache_trigger = CronTrigger(minute="*/5", timezone="UTC")
        scheduler.add_job(refresh_jira_issues_cache, jira_cache_trigger)

        scheduler.start()

        # Initial cache population
        self.refresh_pr_cache()
        refresh_jira_issues_cache()

    def polled_digest_sending(self):
        # send_artefact_summaries(self)
        self.send_team_pr_summaries()

    def _format_story_points(self, story_points) -> str:
        """
        Format story points as whole numbers, handling None values.
        Returns formatted string like "(5 story points)" or empty string if None/0.
        """
        if story_points is None or story_points == 0:
            return ""
        # Convert to int to remove decimal places
        sp_value = int(story_points)
        # Use singular or plural form
        if sp_value == 1:
            return f" ({sp_value} story point)"
        else:
            return f" ({sp_value} story points)"

    def _format_pr_link(self, pr, github_org: str) -> str:
        """
        Format PR link as [org]/[repo] #[PR number] linking to the PR.
        Returns formatted string like "[canonical]/[checkbox] #123"
        """
        repo_name = pr.get("repository", "unknown")
        pr_number = pr.get("number", "unknown")
        html_url = pr.get("html_url", "")
        
        return f"[{github_org}/{repo_name} #{pr_number}]({html_url})"

    def _format_pr_summary(
        self, github_username: str, pr_data: dict, is_digest: bool = False, mattermost_handle: str = None
    ) -> str | None:
        """
        Format PR summary message for a user. Shared between !prs command and digest.

        Args:
            github_username: GitHub username
            pr_data: Dict with 'assigned', 'authored_unassigned', 'authored_approved', and 'authored_changes_requested' PR lists
            is_digest: True for digest format, False for command response
            mattermost_handle: Optional Mattermost handle for digest greeting

        Returns:
            Formatted message string
        """
        prs_assigned_to_user = pr_data[
            "assigned"
        ]  # These are PRs where user is requested reviewer or assignee
        authored_prs_with_no_assignment = pr_data["authored_unassigned"]
        authored_approved_prs = pr_data.get("authored_approved", [])
        authored_changes_requested_prs = pr_data.get("authored_changes_requested", [])
        authored_pending_review_prs = pr_data.get("authored_pending_review", [])

        if (
            not prs_assigned_to_user
            and not authored_prs_with_no_assignment
            and not authored_approved_prs
            and not authored_changes_requested_prs
            and not authored_pending_review_prs
        ):
            if is_digest:
                return None  # Skip digest for users with no PRs
            else:
                cache_stats = self.pr_cache.get_cache_stats()
                return f"No PRs with @{github_username} as requested reviewer or assignee, and no unassigned, approved, or changes requested PRs authored by @{github_username} across {cache_stats['total_repositories']} repositories in {github_org}."

        if is_digest:
            # Use Mattermost handle for greeting if provided, otherwise fall back to GitHub username
            greeting_name = mattermost_handle if mattermost_handle else github_username
            msg = f"Hello @{greeting_name}!\n\n"
        else:
            msg = ""

        if prs_assigned_to_user:
            msg += "**PRs pending your review:**\n"
            for pr in prs_assigned_to_user:
                repo_name = pr.get("repository", "unknown")
                user_roles = pr.get("user_role", [])
                role_indicator = ""
                if user_roles:
                    if "reviewer" in user_roles and "assignee" in user_roles:
                        role_indicator = " (reviewer + assignee)"
                    elif "reviewer" in user_roles:
                        role_indicator = " (reviewer)"
                    elif "assignee" in user_roles:
                        role_indicator = " (assignee)"

                pr_link = self._format_pr_link(pr, github_org)
                if is_digest:
                    msg += f"- [{pr['title']}]({pr['html_url']}) {pr_link}{role_indicator}\n"
                else:
                    msg += f"- {pr_link}: {pr['title']}{role_indicator}\n"
            msg += "\n" if is_digest else ""

        if authored_prs_with_no_assignment:
            if not is_digest and prs_assigned_to_user:
                msg += "\n"
            msg += "**The following PRs you authored presently lack an assigned reviewer:**\n"
            for pr in authored_prs_with_no_assignment:
                pr_link = self._format_pr_link(pr, github_org)
                if is_digest:
                    msg += f"- [{pr['title']}]({pr['html_url']}) {pr_link}\n"
                else:
                    msg += f"- {pr_link}: {pr['title']}\n"
            msg += "\n" if is_digest else ""

        if authored_pending_review_prs:
            if not is_digest and (
                prs_assigned_to_user or authored_prs_with_no_assignment
            ):
                msg += "\n"
            msg += "**PRs you authored that are awaiting review:**\n"
            for pr in authored_pending_review_prs:
                pr_link = self._format_pr_link(pr, github_org)
                if is_digest:
                    msg += f"- [{pr['title']}]({pr['html_url']}) {pr_link}\n"
                else:
                    msg += f"- {pr_link}: {pr['title']}\n"
            msg += "\n" if is_digest else ""

        if authored_changes_requested_prs:
            if not is_digest and (
                prs_assigned_to_user or authored_prs_with_no_assignment or authored_pending_review_prs
            ):
                msg += "\n"
            msg += "**PRs you authored where changes have been requested:**\n"
            for pr in authored_changes_requested_prs:
                pr_link = self._format_pr_link(pr, github_org)
                if is_digest:
                    msg += f"- [{pr['title']}]({pr['html_url']}) {pr_link}\n"
                else:
                    msg += f"- {pr_link}: {pr['title']}\n"
            msg += "\n" if is_digest else ""

        if authored_approved_prs:
            if not is_digest and (
                prs_assigned_to_user or authored_prs_with_no_assignment or authored_pending_review_prs or authored_changes_requested_prs
            ):
                msg += "\n"
            msg += "**Approved PRs, pending merge:**\n"
            for pr in authored_approved_prs:
                pr_link = self._format_pr_link(pr, github_org)
                if is_digest:
                    msg += f"- [{pr['title']}]({pr['html_url']}) {pr_link}\n"
                else:
                    msg += f"- {pr_link}: {pr['title']}\n"

        return msg

    def _get_github_username_for_user(self, mattermost_username: str) -> str | None:
        """
        Helper method to get GitHub username from Mattermost username.
        Shared between commands to avoid duplication.
        """
        try:
            github_username = get_github_username_from_mattermost_handle(
                mattermost_username
            )

            if not github_username:
                # Fallback to email-based lookup
                target_user_email = get_email_from_mattermost_handle(
                    mattermost_username
                )
                if target_user_email:
                    github_username = get_github_username_from_email(
                        github_token, target_user_email
                    )

            return github_username
        except Exception as e:
            logger.warning(
                f"Error looking up GitHub username for @{mattermost_username}: {e}"
            )
            return None

    def _generate_user_digest(
        self, github_username: str, mattermost_username: str, is_digest: bool = False
    ) -> str | None:
        """
        Generate a combined PR and Jira digest for a user.
        Shared between !digest command and daily digest.
        """
        try:
            # Get PR data for this user
            pr_data = self.pr_cache.get_prs_for_user(github_username)

            # Format PR message using shared logic
            pr_msg = self._format_pr_summary(
                github_username, pr_data, is_digest=is_digest, mattermost_handle=mattermost_username
            )

            # Get Jira issues for this user
            jira_issues = get_jira_issues_for_mattermost_handle(mattermost_username)
            jira_msg = None

            if jira_issues["active"] or jira_issues.get("review", []) or jira_issues["completed"] or jira_issues.get("untriaged", []):
                # Calculate story point totals (as whole numbers)
                active_sp = int(sum(issue['story_points'] or 0 for issue in jira_issues["active"]))
                review_sp = int(sum(issue['story_points'] or 0 for issue in jira_issues.get("review", [])))
                completed_sp = int(sum(issue['story_points'] or 0 for issue in jira_issues["completed"]))
                untriaged_sp = int(sum(issue['story_points'] or 0 for issue in jira_issues.get("untriaged", [])))
                total_sp = active_sp + review_sp + completed_sp + untriaged_sp
                
                jira_msg = "**Your Jira issues:**\n\n"

                if jira_issues["active"]:
                    active_sp_text = "story point" if active_sp == 1 else "story points"
                    jira_msg += f"**Active ({active_sp} {active_sp_text}):**\n"
                    for issue in jira_issues["active"]:
                        story_points = self._format_story_points(issue['story_points'])
                        jira_msg += f"- {issue['priority']}: [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points}\n"
                        jira_msg += f"  Status: {issue['status']}\n"
                    jira_msg += "\n"

                if jira_issues.get("review", []):
                    review_sp_text = "story point" if review_sp == 1 else "story points"
                    jira_msg += f"**In Review ({review_sp} {review_sp_text}):**\n"
                    for issue in jira_issues["review"]:
                        story_points = self._format_story_points(issue['story_points'])
                        jira_msg += f"- {issue['priority']}: [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points}\n"
                        jira_msg += f"  Status: {issue['status']}\n"
                    jira_msg += "\n"

                if jira_issues["completed"]:
                    completed_sp_text = "story point" if completed_sp == 1 else "story points"
                    jira_msg += f"**Recently Completed ({completed_sp} {completed_sp_text}):**\n"
                    completed_links = []
                    for issue in jira_issues["completed"]:
                        # Format: Priority: [KEY](url "Title")
                        completed_links.append(f"{issue['priority']}: [{issue['key']}]({issue['url']} \"{issue['summary']}\")")
                    jira_msg += "- " + ", ".join(completed_links) + "\n\n"

                if jira_issues.get("untriaged", []):
                    untriaged_sp_text = "story point" if untriaged_sp == 1 else "story points"
                    jira_msg += f"**⚠️ Untriaged issues in the active pulse ({untriaged_sp} {untriaged_sp_text}):**\n"
                    jira_msg += "*These should either have been triaged or should not be in the current pulse*\n"
                    for issue in jira_issues["untriaged"]:
                        story_points = self._format_story_points(issue['story_points'])
                        jira_msg += f"- [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points}\n"
                        jira_msg += f"  Status: {issue['status']}\n"
                    jira_msg += "\n"
                
                # Add total summary if there are any issues
                total_sp_text = "story point" if total_sp == 1 else "story points"
                jira_msg += f"**Total: {total_sp} {total_sp_text}**\n"

            # Combine PR and Jira messages
            combined_msg = ""
            if pr_msg:
                combined_msg += pr_msg
            if jira_msg:
                if combined_msg:
                    combined_msg += "\n\n"
                combined_msg += jira_msg

            return combined_msg if combined_msg else None

        except Exception as e:
            logger.error(f"Error generating digest for {github_username}: {e}")
            return None

    def send_team_pr_summaries(self):
        """
        Send daily summaries (PRs + Jira issues) to all members of the configured GitHub team.
        """
        if not github_team:
            logger.debug("No GitHub team configured, skipping team PR summaries")
            return

        try:
            # Get team members
            team_members = self.pr_cache.get_team_members(github_team)
            if not team_members:
                logger.warning(f"No members found for team {github_team}")
                return

            logger.info(
                f"Sending daily summaries (PRs + Jira) to {len(team_members)} team members"
            )

            for github_username in team_members:
                logger.info(f"Sending daily summary to {github_username}")

                try:
                    # Get Mattermost username for this GitHub user
                    mattermost_handle = get_mattermost_handle_from_github_username(
                        github_username
                    )
                    if not mattermost_handle:
                        mattermost_handle = github_username  # Fallback
                        logger.warning(
                            f"Could not find Mattermost handle for {github_username}, using GitHub username"
                        )

                    # Generate digest using shared logic
                    combined_msg = self._generate_user_digest(
                        github_username, mattermost_handle, is_digest=True
                    )

                    # Skip if no PRs or Jira issues for this user
                    if not combined_msg:
                        logger.info(
                            f"No PRs or Jira issues found for {github_username}, skipping"
                        )
                        continue

                    # Send direct message to user
                    identifier = self.build_identifier(f"@{mattermost_handle}")
                    self.send(identifier, combined_msg)
                    logger.info(f"Sent daily summary (PRs + Jira) to {mattermost_handle} (GitHub: {github_username})")

                except Exception as e:
                    logger.error(
                        f"Error sending daily summary to {github_username}: {e}"
                    )

        except Exception as e:
            logger.error(f"Error sending team PR summaries: {e}")

    def refresh_pr_cache(self):
        """Refresh the PR cache with latest data from filtered repositories"""
        try:
            self.pr_cache.refresh_cache()
            logger.info("PR cache refreshed successfully")
        except Exception as e:
            logger.error(f"Error refreshing PR cache: {e}")

    @botcmd(split_args_with=" ")
    def artefacts(self, msg, args):
        logger.info(
            f"!artefacts command called by {msg.frm.username} with args: {args}"
        )
        try:
            result = reply_with_artefacts_summary(msg.frm, args)
            logger.info(f"!artefacts command returning {len(result)} characters")
            return result
        except Exception as e:
            logger.error(f"Error in !artefacts command: {e}", exc_info=True)
            return f"Error processing artefacts command: {str(e)}"

    @botcmd(split_args_with=" ")
    def prs(self, msg, args):
        """
        List PRs where you are a requested reviewer or assignee, plus unassigned PRs authored by you
        Usage: !prs [mattermost_username]
        Default username: your own username (mapped from LDAP)
        Now searches across ALL repositories in the configured GitHub organization
        """
        # Parse arguments and get GitHub username
        if args and len(args) > 0 and args[0].strip():
            mattermost_username = args[0].lstrip("@")
            github_username = self._get_github_username_for_user(mattermost_username)
            if not github_username:
                return f"Could not find GitHub username for Mattermost user @{mattermost_username}"
        else:
            mattermost_username = msg.frm.username
            github_username = self._get_github_username_for_user(mattermost_username)
            if not github_username:
                github_username = mattermost_username  # Fallback

        if not github_token:
            return "GitHub token not configured. Please set the GITHUB_TOKEN environment variable."

        try:
            # Get PRs for the user from cache
            pr_data = self.pr_cache.get_prs_for_user(github_username)

            # Use shared formatting logic
            response = self._format_pr_summary(
                github_username, pr_data, is_digest=False
            )
            return response

        except Exception as e:
            logger.error(f"Error getting PRs from cache: {e}")
            return f"Error fetching PRs: {str(e)}"

    @botcmd(split_args_with=" ", name="cid")
    def cid(self, msg, args):
        c3_client = C3Client(
            base_url="https://certification.canonical.com", token=c3_access_token
        )

        msg = ""

        with c3_client:
            for cid in args:
                msg += cid
                msg += "\n"

                r = get_physicalmachinesview(client=c3_client, canonical_id=cid)

                for machine in r.parsed:
                    make = machine.make if r.make is not None else "Unknown"
                    model = machine.model if r.model is not None else "Unknown"
                    tf_provision_type = (
                        machine.tf_provision_type
                        if machine.tf_provision_type is not None
                        else "Unknown"
                    )

                    msg = f"{make} | {model} | {tf_provision_type}\n"

            return msg

    @botcmd(split_args_with=" ")
    def jira(self, msg, args):
        """
        List Jira issues assigned to you or another user
        Usage: !jira [mattermost_username]
        Default username: your own username (mapped from LDAP to email)
        """
        mattermost_username = None

        # Parse arguments
        if args and len(args) > 0 and args[0].strip():
            # If Mattermost username is provided
            mattermost_username = args[0].lstrip("@")  # Remove @ prefix if present
        else:
            # Use requesting user's Mattermost username
            mattermost_username = msg.frm.username

        try:
            # Get Jira issues for the user
            issues = get_jira_issues_for_mattermost_handle(mattermost_username)

            if not issues["active"] and not issues.get("review", []) and not issues["completed"] and not issues.get("untriaged", []):
                return f"No Jira issues assigned to @{mattermost_username}"

            # Calculate story point totals (as whole numbers)
            active_story_points = int(sum(
                issue['story_points'] or 0 for issue in issues["active"]
            ))
            review_story_points = int(sum(
                issue['story_points'] or 0 for issue in issues.get("review", [])
            ))
            completed_story_points = int(sum(
                issue['story_points'] or 0 for issue in issues["completed"]
            ))
            untriaged_story_points = int(sum(
                issue['story_points'] or 0 for issue in issues.get("untriaged", [])
            ))
            total_story_points = active_story_points + review_story_points + completed_story_points + untriaged_story_points

            # Format the response
            response = f"**Jira issues assigned to @{mattermost_username} in the current pulse:**\n\n"

            # Show active issues first
            if issues["active"]:
                sp_text = "story point" if active_story_points == 1 else "story points"
                response += f"**Active ({active_story_points} {sp_text}):**\n"
                for issue in issues["active"]:
                    story_points = self._format_story_points(issue['story_points'])
                    response += f"- {issue['priority']}: [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points} ({issue['status']})\n"
                response += "\n"

            # Show issues in review
            if issues.get("review", []):
                sp_text = "story point" if review_story_points == 1 else "story points"
                response += f"**In Review ({review_story_points} {sp_text}):**\n"
                for issue in issues["review"]:
                    story_points = self._format_story_points(issue['story_points'])
                    response += f"- {issue['priority']}: [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points} ({issue['status']})\n"
                response += "\n"

            # Show completed issues separately (compact format)
            if issues["completed"]:
                sp_text = "story point" if completed_story_points == 1 else "story points"
                response += f"**Completed during the pulse ({completed_story_points} {sp_text}):**\n"
                completed_links = []
                for issue in issues["completed"]:
                    # Format: Priority: [KEY](url "Title")
                    completed_links.append(f"{issue['priority']}: [{issue['key']}]({issue['url']} \"{issue['summary']}\")")
                response += "- " + ", ".join(completed_links) + "\n\n"

            # Show untriaged issues (these need attention!)
            if issues.get("untriaged", []):
                sp_text = "story point" if untriaged_story_points == 1 else "story points"
                response += f"**⚠️ Untriaged issues in the active pulse ({untriaged_story_points} {sp_text}):**\n"
                response += "*These should either have been triaged or should not be in the current pulse*\n"
                for issue in issues["untriaged"]:
                    story_points = self._format_story_points(issue['story_points'])
                    response += f"- [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points} ({issue['status']})\n"
                response += "\n"

            # Add total summary
            total_sp_text = "story point" if total_story_points == 1 else "story points"
            response += f"**Total: {total_story_points} {total_sp_text}**"
            return response

        except Exception as e:
            logger.error(f"Error fetching Jira issues for {mattermost_username}: {e}")
            return f"Error fetching Jira issues: {str(e)}"

    @botcmd(split_args_with=" ")
    def team_jira(self, msg, args):
        """
        List Jira issues assigned to GitHub team members (displayed with Mattermost handles)
        Usage: !team_jira
        Uses the configured GitHub team
        """
        if not github_team:
            return "No GitHub team configured. Please set the GITHUB_TEAM environment variable."

        try:
            # Get team members (GitHub usernames)
            team_members = self.pr_cache.get_team_members(github_team)
            if not team_members:
                return f"No members found for team {github_team}"

            # Get Jira issues for all team members
            team_issues = get_jira_issues_for_github_team_members(team_members)

            if not team_issues:
                return (
                    f"No open Jira issues assigned to any members of team {github_team}"
                )

            # Format the response
            response = f"**Jira issues assigned to team {github_team}:**\n\n"

            total_active = 0
            total_completed = 0
            total_untriaged = 0
            total_active_sp = 0
            total_completed_sp = 0
            total_untriaged_sp = 0
            
            for github_username, user_issues in team_issues.items():
                if user_issues["active"] or user_issues.get("review", []) or user_issues["completed"] or user_issues.get("untriaged", []):
                    # Calculate user's story points
                    user_active_sp = int(sum(issue['story_points'] or 0 for issue in user_issues["active"]))
                    user_review_sp = int(sum(issue['story_points'] or 0 for issue in user_issues.get("review", [])))
                    user_completed_sp = int(sum(issue['story_points'] or 0 for issue in user_issues["completed"]))
                    user_untriaged_sp = int(sum(issue['story_points'] or 0 for issue in user_issues.get("untriaged", [])))
                    
                    # Get the actual Mattermost handle for this GitHub user
                    mattermost_handle = get_mattermost_handle_from_github_username(
                        github_username
                    )
                    if not mattermost_handle:
                        # Fallback to GitHub username if lookup fails
                        mattermost_handle = github_username
                        logger.warning(
                            f"Could not find Mattermost handle for {github_username}, using GitHub username"
                        )

                    response += f"**@{mattermost_handle}:**\n"

                    # Show active issues
                    if user_issues["active"]:
                        active_sp_text = "story point" if user_active_sp == 1 else "story points"
                        response += f"  *Active ({user_active_sp} {active_sp_text}):*\n"
                        for issue in user_issues["active"]:
                            story_points = self._format_story_points(issue['story_points'])
                            response += f"  - {issue['priority']}: [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points}\n"
                            response += f"    Status: {issue['status']}\n"
                        total_active += len(user_issues["active"])
                        total_active_sp += user_active_sp

                    # Show review issues
                    if user_issues.get("review", []):
                        review_sp_text = "story point" if user_review_sp == 1 else "story points"
                        response += f"  *In Review ({user_review_sp} {review_sp_text}):*\n"
                        for issue in user_issues["review"]:
                            story_points = self._format_story_points(issue['story_points'])
                            response += f"  - {issue['priority']}: [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points}\n"
                            response += f"    Status: {issue['status']}\n"
                        total_active += len(user_issues["review"])  # Count review as active
                        total_active_sp += user_review_sp

                    # Show completed issues (compact format)
                    if user_issues["completed"]:
                        completed_sp_text = "story point" if user_completed_sp == 1 else "story points"
                        response += f"  *Recently Completed ({user_completed_sp} {completed_sp_text}):*\n"
                        completed_links = []
                        for issue in user_issues["completed"]:
                            # Format: Priority: [KEY](url "Title")
                            completed_links.append(f"{issue['priority']}: [{issue['key']}]({issue['url']} \"{issue['summary']}\")")
                        response += "  - " + ", ".join(completed_links) + "\n"
                        total_completed += len(user_issues["completed"])
                        total_completed_sp += user_completed_sp

                    # Show untriaged issues
                    if user_issues.get("untriaged", []):
                        untriaged_sp_text = "story point" if user_untriaged_sp == 1 else "story points"
                        response += f"  *⚠️ Untriaged ({user_untriaged_sp} {untriaged_sp_text}):*\n"
                        for issue in user_issues["untriaged"]:
                            story_points = self._format_story_points(issue['story_points'])
                            response += f"  - [{issue['summary']}]({issue['url']}) `{issue['key']}`{story_points}\n"
                            response += f"    Status: {issue['status']}\n"
                        total_untriaged += len(user_issues["untriaged"])
                        total_untriaged_sp += user_untriaged_sp

                    response += "\n"

            # Format team totals with proper singular/plural
            active_sp_text = "story point" if total_active_sp == 1 else "story points"
            completed_sp_text = "story point" if total_completed_sp == 1 else "story points"
            untriaged_sp_text = "story point" if total_untriaged_sp == 1 else "story points"
            
            response += f"**Total: {total_active} active ({total_active_sp} {active_sp_text}), {total_completed} completed ({total_completed_sp} {completed_sp_text})"
            
            if total_untriaged > 0:
                response += f", {total_untriaged} untriaged ({total_untriaged_sp} {untriaged_sp_text})"
            
            response += " issues**"
            
            if total_untriaged > 0:
                response += f"\n\n⚠️ **Warning: {total_untriaged} untriaged issues need attention!**"
            return response

        except Exception as e:
            logger.error(f"Error fetching team Jira issues: {e}")
            return f"Error fetching team Jira issues: {str(e)}"

    @botcmd(split_args_with=" ")
    def sprint_summary(self, msg, args):
        """
        Generate an AI-powered summary of the current sprint's tasks
        Usage: !sprint_summary
        Uses the configured LLM to analyze and summarize current sprint issues
        """
        try:
            # Check if LLM functionality is available
            if not LLM_AVAILABLE:
                return "LLM functionality not available. Please ensure the requests library is installed and LLM configuration is set up."

            # Get LLM client
            llm_client = get_llm_client()
            if not llm_client:
                return "LLM API not configured. Please set LLM_API_SERVER, and optionally LLM_API_TOKEN and LLM_MODEL_NAME environment variables."

            # Test LLM connection
            if not llm_client.test_connection():
                return f"Could not connect to LLM API at {llm_client.server_url}. Please check the configuration and server status."

            # Get all current sprint issues from cache
            all_sprint_issues = []
            for assignee_email, issues in jira_issues_cache.items():
                for issue in issues:
                    all_sprint_issues.append(
                        {
                            "assignee": assignee_email,
                            "key": issue["key"],
                            "summary": issue["summary"],
                            "status": issue["status"],
                            "priority": issue["priority"],
                            "story_points": issue.get("story_points"),
                            "is_completed": issue.get("is_completed", False),
                        }
                    )

            if not all_sprint_issues:
                return "No sprint issues found in cache. The Jira integration may need to be configured or refreshed."

            # Prepare data for LLM
            active_issues = [
                issue for issue in all_sprint_issues if not issue["is_completed"]
            ]
            completed_issues = [
                issue for issue in all_sprint_issues if issue["is_completed"]
            ]

            # Create structured prompt for the LLM
            prompt = self._create_sprint_summary_prompt(active_issues, completed_issues)

            # Generate summary using LLM
            logger.info(f"Generating sprint summary using {llm_client.model_name}")
            summary = llm_client.generate_completion(
                prompt, max_tokens=2000, temperature=0.3
            )

            if not summary:
                return "Failed to generate sprint summary. The LLM API may be unavailable or returned an empty response."

            # Filter out thinking tags from LLM response
            summary = self._filter_thinking_output(summary)

            # Add metadata
            total_active = len(active_issues)
            total_completed = len(completed_issues)
            total_story_points_active = sum(
                issue.get("story_points") or 0 for issue in active_issues
            )
            total_story_points_completed = sum(
                issue.get("story_points") or 0 for issue in completed_issues
            )

            header = f"**🚀 Current Sprint Summary** (Generated by {llm_client.model_name})\n\n"
            header += "**📊 Sprint Metrics:**\n"
            header += f"- Active Issues: {total_active} ({total_story_points_active} story points)\n"
            header += f"- Completed Issues: {total_completed} ({total_story_points_completed} story points)\n"
            header += f"- Total Issues: {total_active + total_completed}\n\n"

            return header + summary

        except Exception as e:
            logger.error(f"Error generating sprint summary: {e}")
            return f"Error generating sprint summary: {str(e)}"

    def _create_sprint_summary_prompt(self, active_issues, completed_issues):
        """Create a structured prompt for sprint summary generation"""
        prompt = """You are a project manager analyzing the current software development sprint. Please provide a concise, well-structured summary of the sprint progress.

**Active Issues:**
"""

        # Add active issues
        for issue in active_issues[:20]:  # Limit to avoid token overflow
            story_points = (
                f" ({issue['story_points']} SP)" if issue["story_points"] else ""
            )
            assignee = (
                issue["assignee"].split("@")[0]
                if "@" in issue["assignee"]
                else issue["assignee"]
            )
            prompt += f"- {issue['key']}: {issue['summary']} - {issue['status']} ({issue['priority']}){story_points} [Assignee: {assignee}]\n"

        if len(active_issues) > 20:
            prompt += f"... and {len(active_issues) - 20} more active issues\n"

        prompt += "\n**Completed Issues:**\n"

        # Add completed issues
        for issue in completed_issues[:15]:  # Limit completed issues
            story_points = (
                f" ({issue['story_points']} SP)" if issue["story_points"] else ""
            )
            assignee = (
                issue["assignee"].split("@")[0]
                if "@" in issue["assignee"]
                else issue["assignee"]
            )
            prompt += f"- {issue['key']}: {issue['summary']} - {issue['status']} ({issue['priority']}){story_points} [Assignee: {assignee}]\n"

        if len(completed_issues) > 15:
            prompt += f"... and {len(completed_issues) - 15} more completed issues\n"

        prompt += """
Please provide a summary that includes:
1. **Sprint Progress Overview**: Overall progress and momentum
2. **Key Achievements**: Notable completed work
3. **Current Focus Areas**: What the team is actively working on
4. **Potential Blockers**: Any high-priority issues that might need attention
5. **Sprint Health**: Brief assessment of sprint health and velocity

Keep the summary concise (3-4 paragraphs) and actionable for team members and stakeholders. Use a professional but friendly tone."""

        return prompt

    def _filter_thinking_output(self, text):
        """Filter out thinking output from LLM response (text between <think> and </think> tags)"""
        import re

        # Remove everything between <think> and </think> tags (including the tags themselves)
        # Using re.DOTALL to match across multiple lines
        filtered_text = re.sub(
            r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE
        )

        # Clean up any extra whitespace that might be left
        filtered_text = re.sub(
            r"\n\s*\n\s*\n", "\n\n", filtered_text
        )  # Replace multiple blank lines with double newline
        filtered_text = filtered_text.strip()

        return filtered_text

    @botcmd(split_args_with=" ")
    def digest(self, msg, args):
        """
        Show current digest information (equivalent to daily scheduled digest)
        Usage: !digest [mattermost_username]
        Default username: your own username (mapped from LDAP)
        Shows PRs requiring attention, authored unassigned PRs, approved authored PRs, and Jira issues
        """
        # Parse arguments and get usernames
        if args and len(args) > 0 and args[0].strip():
            mattermost_username = args[0].lstrip("@")
            github_username = self._get_github_username_for_user(mattermost_username)
            if not github_username:
                return f"Could not find GitHub username for Mattermost user @{mattermost_username}"
        else:
            mattermost_username = msg.frm.username
            github_username = self._get_github_username_for_user(mattermost_username)
            if not github_username:
                github_username = mattermost_username  # Fallback

        if not github_token:
            return "GitHub token not configured. Please set the GITHUB_TOKEN environment variable."

        try:
            # Generate digest using shared logic
            combined_msg = self._generate_user_digest(
                github_username, mattermost_username, is_digest=False
            )

            # Return the digest or no content message
            if combined_msg:
                return combined_msg
            else:
                cache_stats = self.pr_cache.get_cache_stats()
                return f"No PRs or Jira issues found for @{mattermost_username} across {cache_stats['total_repositories']} repositories in {github_org}."

        except Exception as e:
            logger.error(f"Error generating digest: {e}")
            return f"Error generating digest: {str(e)}"
