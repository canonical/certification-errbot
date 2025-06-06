import os
from datetime import datetime
import logging

from dotenv import load_dotenv
from errbot import BotPlugin, botcmd, re_botcmd

from c3.client import AuthenticatedClient as C3Client
from c3.api.physicalmachinesview.physicalmachinesview_list import sync_detailed as get_physicalmachinesview
from c3_auth import get_access_token as get_c3_access_token
from artefacts import reply_with_artefacts_summary, send_artefact_summaries
from ldap import get_github_username_from_mattermost_handle, get_email_from_mattermost_handle
from github import get_github_username_from_email
from pr_cache import PullRequestCache

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import ssl_fix

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

if not c3_client_id or not c3_client_secret:
    raise Exception("C3_CLIENT_ID and C3_CLIENT_SECRET must be set")

if not github_token:
    raise Exception("GITHUB_TOKEN must be set")

if not github_org:
    raise Exception("GITHUB_ORG must be set")

C3_BASE_URL = 'https://certification.canonical.com'

c3_access_token = get_c3_access_token(C3_BASE_URL, c3_client_id, c3_client_secret)

now = datetime.now().date()

# Default repositories to monitor for PRs
DEFAULT_REPOS = [
    "blueprints",
    "certification-docs",
    "certification-lab-ci",
    "certification-lab-manager",
    "certification-ops",
    "charm-integration-testing",
    "checkbox",
    "fcbtest",
    "hardware-api",
    "hexr",
    "hwcert-jenkins-jobs",
    "hwcert-jenkins-tools",
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
    "yarf",
]

# Get repositories from environment variable or use defaults
github_repositories_env = os.environ.get("GITHUB_REPOSITORIES")
if github_repositories_env:
    GITHUB_REPOS = [repo.strip() for repo in github_repositories_env.split(',') if repo.strip()]
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
        
        # Daily artefact digest (Mon-Fri 9:00 UTC)
        digest_trigger = CronTrigger(day_of_week='mon-fri', hour=9, minute=00, timezone='UTC')
        scheduler.add_job(self.polled_digest_sending, digest_trigger)

        # PR cache refresh (every 5 minutes)
        pr_cache_trigger = CronTrigger(minute='*/5', timezone='UTC')
        scheduler.add_job(self.refresh_pr_cache, pr_cache_trigger)
        
        scheduler.start()
        
        # Initial PR cache population
        self.refresh_pr_cache()

    def polled_digest_sending(self):
        send_artefact_summaries(self)
        self.send_team_pr_summaries()
    
    def _format_pr_summary(self, github_username: str, pr_data: dict, is_digest: bool = False) -> str:
        """
        Format PR summary message for a user. Shared between !prs command and digest.
        
        Args:
            github_username: GitHub username
            pr_data: Dict with 'assigned' and 'authored_unassigned' PR lists
            is_digest: True for digest format, False for command response
        
        Returns:
            Formatted message string
        """
        prs_requested_to_review = pr_data["assigned"]  # These are PRs where user is in requested_reviewers
        authored_prs_with_no_requested_reviewer = pr_data["authored_unassigned"]
        
        if not prs_requested_to_review and not authored_prs_with_no_requested_reviewer:
            if is_digest:
                return None  # Skip digest for users with no PRs
            else:
                cache_stats = self.pr_cache.get_cache_stats()
                return f"No PRs with @{github_username} as requested reviewer and no unassigned PRs authored by @{github_username} across {cache_stats['total_repositories']} repositories in {github_org}."
        
        if is_digest:
            msg = f"Good morning @{github_username}! Here's your daily PR summary:\n\n"
        else:
            msg = ""
        
        if prs_requested_to_review:
            msg += f"**PRs pending review from @{github_username}:**\n"
            for pr in prs_requested_to_review:
                repo_name = pr.get("repository", "unknown")
                if is_digest:
                    msg += f"- [{pr['title']}]({pr['html_url']}) ({repo_name})\n"
                else:
                    msg += f"- [{pr['html_url']}]({pr['html_url']}) ({repo_name}): {pr['title']}\n"
            msg += "\n" if is_digest else ""
        
        if authored_prs_with_no_requested_reviewer:
            if not is_digest and prs_requested_to_review:
                msg += "\n"
            msg += f"**PRs authored by @{github_username} with no reviewer assigned:**\n"
            for pr in authored_prs_with_no_requested_reviewer:
                repo_name = pr.get("repository", "unknown")
                if is_digest:
                    msg += f"- [{pr['title']}]({pr['html_url']}) ({repo_name})\n"
                else:
                    msg += f"- [{pr['html_url']}]({pr['html_url']}) ({repo_name}): {pr['title']}\n"
        
        return msg

    def send_team_pr_summaries(self):
        """
        Send daily PR summaries to all members of the configured GitHub team.
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
                
            logger.info(f"Sending PR summaries to {len(team_members)} team members")
            
            for github_username in team_members:
                logger.info(f"Sending PR summary to {github_username}")

                try:
                    # Get PR data for this user
                    pr_data = self.pr_cache.get_prs_for_user(github_username)
                    
                    # Format message using shared logic
                    msg = self._format_pr_summary(github_username, pr_data, is_digest=True)
                    
                    # Skip if no PRs for this user
                    if not msg:
                        logger.info(f"No PRs found for {github_username}, skipping")
                        continue
                    
                    # Send direct message to user
                    identifier = self.build_identifier(f"@{github_username}")
                    self.send(identifier, msg)
                    logger.info(f"Sent PR summary to {github_username}")
                    
                except Exception as e:
                    logger.error(f"Error sending PR summary to {github_username}: {e}")
                    
        except Exception as e:
            logger.error(f"Error sending team PR summaries: {e}")
    
    def refresh_pr_cache(self):
        """Refresh the PR cache with latest data from filtered repositories"""
        try:
            self.pr_cache.refresh_cache()
            logger.info("PR cache refreshed successfully")
        except Exception as e:
            logger.error(f"Error refreshing PR cache: {e}")
        

    @botcmd(split_args_with=' ')
    def artefacts(self, msg, args):
        return reply_with_artefacts_summary(self, msg.frm, args)

    @botcmd(split_args_with=" ")
    def prs(self, msg, args):
        """
        List PRs where you are a requested reviewer or another user, plus unassigned PRs authored by you
        Usage: !prs [mattermost_username]
        Default username: your own username (mapped from LDAP)
        Now searches across ALL repositories in the configured GitHub organization
        """
        github_username = None
        
        # Parse arguments
        if args and len(args) > 0 and args[0].strip():
            # If Mattermost username is provided, map to GitHub via LDAP
            mattermost_username = args[0].lstrip('@')  # Remove @ prefix if present
            try:
                github_username = get_github_username_from_mattermost_handle(mattermost_username)
                
                if not github_username:
                    # Fallback to email-based lookup
                    target_user_email = get_email_from_mattermost_handle(mattermost_username)
                    if target_user_email:
                        github_username = get_github_username_from_email(github_token, target_user_email)
                
                if not github_username:
                    return f"Could not find GitHub username for Mattermost user @{mattermost_username}"
                    
                logger.info(f"Found GitHub username {github_username} for Mattermost user @{mattermost_username}")
            except Exception as e:
                return f"Could not find Mattermost user @{mattermost_username}: {str(e)}"
        else:
            # Map requesting user's Mattermost account to GitHub username via LDAP
            requesting_user_handle = msg.frm.username
            try:
                github_username = get_github_username_from_mattermost_handle(requesting_user_handle)
                
                if not github_username:
                    # Fallback to email-based lookup
                    target_user_email = get_email_from_mattermost_handle(requesting_user_handle)
                    if target_user_email:
                        github_username = get_github_username_from_email(github_token, target_user_email)
                    
                if not github_username:
                    # Final fallback to using Mattermost username
                    github_username = requesting_user_handle
                    
                logger.info(f"Found GitHub username {github_username} for requesting user @{requesting_user_handle}")
            except Exception as e:
                logger.warning(f"Could not find GitHub username for requesting user @{requesting_user_handle}: {str(e)}")
                # Fallback to using Mattermost username directly
                github_username = requesting_user_handle
            
        if not github_token:
            return "GitHub token not configured. Please set the GITHUB_TOKEN environment variable."
        
        try:
            # Get PRs for the user from cache
            pr_data = self.pr_cache.get_prs_for_user(github_username)
            
            # Log the findings
            prs_requested_to_review = pr_data["assigned"]
            authored_prs_with_no_requested_reviewer = pr_data["authored_unassigned"]
            
            # Determine if we're looking at the requesting user's PRs or someone else's
            is_self = not (args and len(args) > 0 and args[0].strip())  # No meaningful argument means looking at own PRs
            user_prefix = "you" if is_self else f"@{args[0].lstrip('@')}"

            logger.info(f"PRs requesting review from {user_prefix}: {len(prs_requested_to_review)} found")
            logger.info(f"Authored unassigned PRs for {user_prefix}: {len(authored_prs_with_no_requested_reviewer)} found")
            
            # Use shared formatting logic
            response = self._format_pr_summary(github_username, pr_data, is_digest=False)
            return response
            
        except Exception as e:
            logger.error(f"Error getting PRs from cache: {e}")
            return f"Error fetching PRs: {str(e)}"

    @botcmd(split_args_with=" ", name="cid")
    def cid(self, msg, args):
        c3_client = C3Client(base_url='https://certification.canonical.com', token=c3_access_token)

        msg = ""

        with c3_client:
            for cid in args:
                msg += cid
                msg += "\n"

                r = get_physicalmachinesview(client=c3_client, canonical_id=cid)

                for machine in r.parsed:
                    make = machine.make if r.make is not None else "Unknown"
                    model = machine.model if r.model is not None else "Unknown"
                    tf_provision_type = machine.tf_provision_type if machine.tf_provision_type is not None else "Unknown"

                    msg = f"{make} | {model} | {tf_provision_type}\n"

            return msg

