import os
from datetime import datetime
import requests
import logging

from dotenv import load_dotenv
from errbot import BotPlugin, botcmd, re_botcmd

# Load environment variables from .env file if present
load_dotenv()

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

logger = logging.getLogger(__name__)


c3_client_id = os.environ.get("C3_CLIENT_ID")
c3_client_secret = os.environ.get("C3_CLIENT_SECRET")

mattermost_token = os.environ.get("ERRBOT_TOKEN")
mattermost_base_url = f"https://{os.environ.get('ERRBOT_SERVER')}/api/v4"
github_token = os.environ.get("GITHUB_TOKEN")
github_org = os.environ.get("GITHUB_ORG")

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
    "hardware-api",
    "hexr",
    "hwcert-jenkins-jobs",
    "hwcert-jenkins-tools",
    "openapi-rest-proxy",
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
    "zapper"
]


class CertificationPlugin(BotPlugin):
    """
    A plugin for interacting with Certification things
    """
    def __init__(self, bot, name):
        super().__init__(bot, name)
        # Initialize PR cache with default repository filter
        self.pr_cache = PullRequestCache(repo_filter=DEFAULT_REPOS)
    
    def activate(self):
        super().activate()

        scheduler = BackgroundScheduler()
        
        # Daily artefact digest (Mon-Fri 9:00 UTC)
        digest_trigger = CronTrigger(day_of_week='mon-fri', hour=9, minute=00, timezone='UTC')
        scheduler.add_job(self.polled_digest_sending, digest_trigger)
        
        # PR cache refresh (every 15 minutes)
        pr_cache_trigger = CronTrigger(minute='*/2', timezone='UTC')
        scheduler.add_job(self.refresh_pr_cache, pr_cache_trigger)
        
        scheduler.start()
        
        # Initial PR cache population
        self.refresh_pr_cache()

    def polled_digest_sending(self):
        send_artefact_summaries(self)
    
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
        List PRs assigned to you or another user, plus unassigned PRs authored by you
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
            prs_requested_to_review = pr_data["assigned"]
            authored_prs_with_no_requested_reviewer = pr_data["authored_unassigned"]
            
            # Determine if we're looking at the requesting user's PRs or someone else's
            is_self = not (args and len(args) > 0 and args[0].strip())  # No meaningful argument means looking at own PRs
            user_prefix = "you" if is_self else f"@{args[0].lstrip('@')}"

            logger.info(f"Assigned PRs for {user_prefix}: {len(prs_requested_to_review)} found")
            logger.info(f"Authored unassigned PRs for {user_prefix}: {len(authored_prs_with_no_requested_reviewer)} found")
            
            if not prs_requested_to_review and not authored_prs_with_no_requested_reviewer:
                cache_stats = self.pr_cache.get_cache_stats()
                return f"No PRs assigned to {user_prefix} and no unassigned PRs authored by {user_prefix} across {cache_stats['total_repositories']} repositories in {github_org}."
            
            response = ""
            
            if prs_requested_to_review:
                response += f"PRs pending review from {user_prefix}:\n\n"
                for pr in prs_requested_to_review:
                    repo_name = pr.get("repository", "unknown")
                    response += f"- [{pr['html_url']}]({pr['html_url']}) ({repo_name}): {pr['title']}\n"
            
            if authored_prs_with_no_requested_reviewer:
                if response:
                    response += "\n"
                response += f"PRs authored by {user_prefix} with no reviewer assigned:\n\n"
                for pr in authored_prs_with_no_requested_reviewer:
                    repo_name = pr.get("repository", "unknown")
                    response += f"- [{pr['html_url']}]({pr['html_url']}) ({repo_name}): {pr['title']}\n"

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

