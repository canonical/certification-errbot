# ruff: noqa: I001, E402

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
from artefacts import (
    archive_artefact_by_id,
    extract_artefact_id_from_url,
    reply_with_artefacts_summary,
)
from ldap import (
    get_github_username_from_mattermost_handle,
    get_email_from_mattermost_handle,
    get_mattermost_handle_from_github_username,
)
from github import get_github_username_from_email
from pr_cache import PullRequestCache
from jira_integration import (
    get_jira_issues_for_mattermost_handle,
    get_jira_issues_for_github_team_members,
    refresh_jira_issues_cache,
    jira_issues_cache,
)
from formatting import (
    format_pr_summary,
    format_pr_link,
    format_jira_summary,
    format_team_jira_summary,
    format_story_points,
    generate_user_digest,
)

logger = logging.getLogger(__name__)

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

load_dotenv()


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

# Lazy loading of c3_access_token - will be initialized when first needed
c3_access_token = None

def get_c3_token():
    """Get or initialize the C3 access token."""
    global c3_access_token
    if c3_access_token is None:
        c3_access_token = get_c3_access_token(C3_BASE_URL, c3_client_id, c3_client_secret)
    return c3_access_token

now = datetime.now().date()

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
        self.pr_cache = PullRequestCache(repo_filter=GITHUB_REPOS)

    def activate(self):
        super().activate()

        scheduler = BackgroundScheduler()

        # Parse the digest send time from config
        try:
            hour, minute = map(int, DIGEST_SEND_TIME.split(":"))
        except ValueError:
            hour, minute = 6, 30
            self.log.warning(
                f"Invalid DIGEST_SEND_TIME format: {DIGEST_SEND_TIME}, using default 6:30"
            )

        digest_trigger = CronTrigger(
            day_of_week="mon-fri", hour=hour, minute=minute, timezone="UTC"
        )
        scheduler.add_job(self.polled_digest_sending, digest_trigger)
        self.log.info(f"Scheduled daily digest for {hour:02d}:{minute:02d} UTC")

        pr_cache_trigger = CronTrigger(minute="*/5", timezone="UTC")
        scheduler.add_job(self.refresh_pr_cache, pr_cache_trigger)

        jira_cache_trigger = CronTrigger(minute="*/5", timezone="UTC")
        scheduler.add_job(refresh_jira_issues_cache, jira_cache_trigger)

        scheduler.start()

        self.refresh_pr_cache()
        refresh_jira_issues_cache()

    def polled_digest_sending(self):
        # Note: artefacts are now included in send_team_pr_summaries
        # send_artefact_summaries(self)  # Can be enabled for separate artefact-only digest
        self.send_team_pr_summaries()

    def _format_story_points(self, story_points) -> str:
        """
        Format story points as whole numbers, handling None values.
        Returns formatted string like "(5 story points)" or empty string if None/0.
        """
        return format_story_points(story_points)

    def _format_pr_link(self, pr, github_org: str) -> str:
        """
        Format PR link as [org]/[repo] #[PR number] linking to the PR.
        Returns formatted string like "[canonical]/[checkbox] #123"
        """
        return format_pr_link(pr, github_org)

    def _format_pr_summary(
        self,
        github_username: str,
        pr_data: dict,
        is_digest: bool = False,
        mattermost_handle: str = None,
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
        # Use the new formatting module
        return format_pr_summary(github_username, pr_data, github_org, is_digest)

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
        self, github_username: str, mattermost_username: str, is_digest: bool = False, use_github_for_jira: bool = False
    ) -> str | None:
        """
        Generate a combined PR and Jira digest for a user.
        Shared between !digest command and daily digest.
        
        Args:
            github_username: GitHub username
            mattermost_username: Mattermost username (may be GitHub username as fallback)
            is_digest: True for digest format, False for command response
            use_github_for_jira: If True, lookup Jira issues via GitHub username->email instead of Mattermost handle
        """
        try:
            pr_data = self.pr_cache.get_prs_for_user(github_username)
            
            # Use the new generate_user_digest function from formatting module
            return generate_user_digest(
                github_username,
                mattermost_username,
                pr_data,
                github_org,
                use_github_for_jira
            )
        except Exception as e:
            logger.error(f"Error generating digest for {github_username}: {e}")
            return None

    def send_team_pr_summaries(self):
        """
        Send daily summaries (PRs + Jira issues + artefacts) to all members of the configured GitHub team.
        """
        if not github_team:
            logger.warning("No GitHub team configured, skipping team PR summaries")
            return

        try:
            team_members = self.pr_cache.get_team_members(github_team)
            if not team_members:
                logger.warning(f"No members found for team {github_team}")
                return


            for github_username in team_members:

                try:
                    mattermost_handle = get_mattermost_handle_from_github_username(
                        github_username
                    )
                    if not mattermost_handle:
                        logger.warning(
                            f"Could not find Mattermost handle for {github_username}, skipping digest"
                        )
                        continue

                    sections = []
                    
                    # Get PR and Jira digest
                    pr_jira_msg = self._generate_user_digest(
                        github_username, mattermost_handle, is_digest=True, use_github_for_jira=True
                    )
                    if pr_jira_msg:
                        sections.append(pr_jira_msg)
                    
                    # Get artefacts for the user  
                    # Create a mock message object with the user info for reply_with_artefacts_summary
                    mock_msg_frm = type('obj', (object,), {'username': mattermost_handle})()
                    artefacts_msg = reply_with_artefacts_summary(mock_msg_frm, [mattermost_handle])
                    if artefacts_msg and not artefacts_msg.startswith("No pending artefacts"):
                        sections.append(artefacts_msg)
                    
                    if not sections:
                        continue
                    
                    combined_msg = "\n\n---\n\n".join(sections)
                    identifier = self.build_identifier(f"@{mattermost_handle}")
                    self.send(identifier, combined_msg)

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
        except Exception as e:
            logger.error(f"Error refreshing PR cache: {e}")

    @botcmd(split_args_with=" ")
    def artefacts(self, msg, args):
        try:
            result = reply_with_artefacts_summary(msg.frm, args)
            return result
        except Exception as e:
            logger.error(f"Error in !artefacts command: {e}", exc_info=True)
            return f"Error processing artefacts command: {str(e)}"
    
    @botcmd(split_args_with=" ", admin_only=True)
    def archive_artefact(self, msg, args):
        """
        Archive an artefact by ID or URL (admin only).
        
        Usage: 
            !archive_artefact <artefact_id> [comment]
            !archive_artefact <test_observer_url> [comment]
        
        Examples:
            !archive_artefact 123
            !archive_artefact 123 "No longer needed"
            !archive_artefact https://test-observer.canonical.com/#/snaps/456
            !archive_artefact https://test-observer.canonical.com/#/debs/789 "Obsolete version"
        """
        if not args:
            return (
                "Usage: !archive_artefact <artefact_id_or_url> [comment]\n"
                "Examples:\n"
                "  !archive_artefact 123\n"
                "  !archive_artefact https://test-observer.canonical.com/#/snaps/456\n"
                "  !archive_artefact 123 \"No longer needed\""
            )
        
        try:
            artefact_id = extract_artefact_id_from_url(args[0])
        except ValueError as e:
            return f"Error: {str(e)}. Please provide a valid artefact ID or Test Observer URL."
        
        comment = " ".join(args[1:]) if len(args) > 1 else None
        
        try:
            result = archive_artefact_by_id(artefact_id, comment)
            return result
        except Exception as e:
            logger.error(f"Error archiving artefact {artefact_id}: {e}", exc_info=True)
            return f"Error archiving artefact: {str(e)}"

    @botcmd(split_args_with=" ")
    def prs(self, msg, args):
        """
        List PRs where you are a requested reviewer or assignee, plus unassigned PRs authored by you
        Usage: !prs [mattermost_username]
        Default username: your own username (mapped from LDAP)
        Now searches across ALL repositories in the configured GitHub organization
        """
        if args and len(args) > 0 and args[0].strip():
            mattermost_username = args[0].lstrip("@")
            github_username = self._get_github_username_for_user(mattermost_username)
            if not github_username:
                return f"Could not find GitHub username for Mattermost user @{mattermost_username}"
        else:
            mattermost_username = msg.frm.username
            github_username = self._get_github_username_for_user(mattermost_username)
            if not github_username:
                github_username = mattermost_username

        if not github_token:
            return "GitHub token not configured. Please set the GITHUB_TOKEN environment variable."

        try:
            pr_data = self.pr_cache.get_prs_for_user(github_username)

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
            base_url="https://certification.canonical.com", token=get_c3_token()
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
        mattermost_username = self._parse_username_arg(args, msg.frm.username)

        try:
            issues = get_jira_issues_for_mattermost_handle(mattermost_username)
            
            return format_jira_summary(mattermost_username, issues, show_completed=True)

        except Exception as e:
            logger.error(f"Error fetching Jira issues for {mattermost_username}: {e}")
            return f"Error fetching Jira issues: {str(e)}"
    
    def _parse_username_arg(self, args, default_username):
        """Helper to parse username from command arguments."""
        if args and len(args) > 0 and args[0].strip():
            return args[0].lstrip("@")
        return default_username

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
            team_members = self.pr_cache.get_team_members(github_team)
            if not team_members:
                return f"No members found for team {github_team}"

            team_issues = get_jira_issues_for_github_team_members(team_members)
            if not team_issues:
                return f"No open Jira issues assigned to any members of team {github_team}"
            
            user_handles = self._get_mattermost_handles_for_team(team_members)

            return format_team_jira_summary(github_team, team_issues, user_handles)
        
        except Exception as e:
            logger.error(f"Error fetching team Jira issues: {e}")
            return f"Error fetching team Jira issues: {str(e)}"
    
    def _get_mattermost_handles_for_team(self, team_members):
        """Get Mattermost handles for a list of GitHub usernames."""
        handles = {}
        for github_username in team_members:
            mattermost_handle = get_mattermost_handle_from_github_username(github_username)
            if not mattermost_handle:
                mattermost_handle = github_username  # Fallback
                logger.warning(f"Could not find Mattermost handle for {github_username}")
            handles[github_username] = mattermost_handle
        return handles

    @botcmd(split_args_with=" ")
    def sprint_summary(self, msg, args):
        """
        Generate an AI-powered summary of the current sprint's tasks
        Usage: !sprint_summary
        Uses the configured LLM to analyze and summarize current sprint issues
        """
        try:
            if not LLM_AVAILABLE:
                return "LLM functionality not available. Please ensure the requests library is installed and LLM configuration is set up."

            llm_client = get_llm_client()
            if not llm_client:
                return "LLM API not configured. Please set LLM_API_SERVER, and optionally LLM_API_TOKEN and LLM_MODEL_NAME environment variables."

            if not llm_client.test_connection():
                return f"Could not connect to LLM API at {llm_client.server_url}. Please check the configuration and server status."

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

            active_issues = [
                issue for issue in all_sprint_issues if not issue["is_completed"]
            ]
            completed_issues = [
                issue for issue in all_sprint_issues if issue["is_completed"]
            ]

            prompt = self._create_sprint_summary_prompt(active_issues, completed_issues)

            summary = llm_client.generate_completion(
                prompt, max_tokens=2000, temperature=0.3
            )

            if not summary:
                return "Failed to generate sprint summary. The LLM API may be unavailable or returned an empty response."

            summary = self._filter_thinking_output(summary)

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

        for issue in active_issues[:20]:
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

        for issue in completed_issues[:15]:
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

        filtered_text = re.sub(
            r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE
        )

        filtered_text = re.sub(
            r"\n\s*\n\s*\n", "\n\n", filtered_text
        )
        filtered_text = filtered_text.strip()

        return filtered_text

    @botcmd(split_args_with=" ")
    def digest(self, msg, args):
        """
        Show current digest information (equivalent to daily scheduled digest)
        Usage: !digest [mattermost_username]
        Default username: your own username (mapped from LDAP)
        Shows PRs requiring attention, authored unassigned PRs, approved authored PRs, Jira issues, and pending artefacts
        """
        if args and len(args) > 0 and args[0].strip():
            mattermost_username = args[0].lstrip("@")
            github_username = self._get_github_username_for_user(mattermost_username)
            if not github_username:
                return f"Could not find GitHub username for Mattermost user @{mattermost_username}"
        else:
            mattermost_username = msg.frm.username
            github_username = self._get_github_username_for_user(mattermost_username)
            if not github_username:
                github_username = mattermost_username

        if not github_token:
            return "GitHub token not configured. Please set the GITHUB_TOKEN environment variable."

        try:
            sections = []
            
            # Get PR and Jira digest
            pr_jira_msg = self._generate_user_digest(
                github_username, mattermost_username, is_digest=False
            )
            if pr_jira_msg:
                sections.append(pr_jira_msg)
            
            # Get artefacts for the user
            artefacts_msg = reply_with_artefacts_summary(msg.frm, [mattermost_username])
            if artefacts_msg and not artefacts_msg.startswith("No pending artefacts"):
                sections.append(artefacts_msg)
            
            if sections:
                return "\n\n---\n\n".join(sections)
            else:
                cache_stats = self.pr_cache.get_cache_stats()
                # Check if we have artefacts even if no PRs/Jira
                if artefacts_msg and not artefacts_msg.startswith("No pending artefacts"):
                    return artefacts_msg
                return f"No PRs, Jira issues, or pending artefacts found for @{mattermost_username} across {cache_stats['total_repositories']} repositories in {github_org}."

        except Exception as e:
            logger.error(f"Error generating digest: {e}")
            return f"Error generating digest: {str(e)}"
