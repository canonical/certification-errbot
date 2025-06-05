from errbot import BotPlugin, botcmd, re_botcmd
import os
from datetime import datetime
import requests

from c3.client import AuthenticatedClient as C3Client
from c3.api.physicalmachinesview.physicalmachinesview_list import sync_detailed as get_physicalmachinesview
from c3_auth import get_access_token as get_c3_access_token
from artefacts import reply_with_artefacts_summary, send_artefact_summaries
from ldap import get_github_username_from_mattermost_handle, get_email_from_mattermost_handle
from github import get_github_username_from_email

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

import ssl_fix

import logging
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

# Predefined list of repositories to check for PRs
DEFAULT_REPOS = [
    "checkbox",
    "testflinger", 
    "hwcert-jenkins-jobs", 
    "certification-docs", 
    "certification-ops"
]

class CertificationPlugin(BotPlugin):
    """
    A plugin for interacting with Certification things
    """
    def __init__(self, bot, name):
        super().__init__(bot, name)
    
    def activate(self):
        super().activate()

        scheduler = BackgroundScheduler()
        trigger = CronTrigger(day_of_week='mon-fri', hour=9, minute=00, timezone='UTC')
        scheduler.add_job(self.polled_digest_sending, trigger)
        scheduler.start()

    def polled_digest_sending(self):
        send_artefact_summaries(self)

    @botcmd(split_args_with=' ')
    def artefacts(self, msg, args):
        return reply_with_artefacts_summary(self, msg.frm, args)

    @botcmd(split_args_with=" ")
    def prs(self, msg, args):
        """
        List PRs assigned to you or another user, plus unassigned PRs authored by you
        Usage: !prs [mattermost_username]
        Default username: your own username (mapped from LDAP)
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
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            prs_requested_to_review = []
            authored_prs_with_no_requested_reviewer = []
            
            # Use predefined repositories with configured organization
            for repo_name in DEFAULT_REPOS:
                # Get PRs assigned to the user
                prs_url = f"https://api.github.com/repos/{github_org}/{repo_name}/pulls?state=open"
                prs_response = requests.get(prs_url, headers=headers)
                
                if prs_response.status_code == 200:
                    prs = prs_response.json()
                    for pr in prs:
                        requested_reviewers = pr.get("requested_reviewers", [])
                        author = pr.get("user", {}).get("login", "")
                        
                        # Check if PR is assigned to the user
                        if any(reviewer["login"].lower() == github_username.lower() for reviewer in requested_reviewers):
                            prs_requested_to_review.append(pr)
                        # Check if PR is authored by user but has no assignees
                        elif author.lower() == github_username.lower() and len(requested_reviewers) == 0:
                            authored_prs_with_no_requested_reviewer.append(pr)
                else:
                    return f"Error fetching PRs from {github_org}/{repo_name}: {prs_response.status_code} - {prs_response.text}"
            
            # Determine if we're looking at the requesting user's PRs or someone else's
            is_self = not (args and len(args) > 0 and args[0].strip())  # No meaningful argument means looking at own PRs
            user_prefix = "you" if is_self else f"@{args[0].lstrip('@')}"

            logger.info(f"Assigned PRs for {user_prefix}: {prs_requested_to_review}")
            logger.info(f"Authored unassigned PRs for {user_prefix}: {authored_prs_with_no_requested_reviewer}")
            
            if not prs_requested_to_review and not authored_prs_with_no_requested_reviewer:
                return f"No PRs assigned to {user_prefix} and no unassigned PRs authored by {user_prefix} in the monitored repositories."
            
            response = ""
            
            if prs_requested_to_review:
                response += f"PRs pending review from {user_prefix}:\n\n"
                for pr in prs_requested_to_review:
                    response += f"- [{pr['html_url']}]({pr['html_url']}): {pr['title']}\n"
            
            if authored_prs_with_no_requested_reviewer:
                if response:
                    response += "\n"
                response += f"PRs authored by {user_prefix} with no reviewer assigned:\n\n"
                for pr in authored_prs_with_no_requested_reviewer:
                    response += f"- [{pr['html_url']}]({pr['html_url']}): {pr['title']}\n"
                
            return response
            
        except requests.exceptions.RequestException as e:
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

