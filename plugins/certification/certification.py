from errbot import BotPlugin, botcmd, re_botcmd
import re
import os
from datetime import date
from datetime import datetime, timedelta

from c3.client import AuthenticatedClient as C3Client
from c3.api.physicalmachinesview.physicalmachinesview_list import sync_detailed as get_physicalmachinesview
from c3.models import PhysicalMachineView
from c3.types import Response
from c3_auth import get_access_token as get_c3_access_token

from test_observer.models import ArtefactDTO, ArtefactStatus, UserDTO
from test_observer.client import Client as TestObserverClient
from test_observer.api.artefacts.get_artefacts_v1_artefacts_get import sync_detailed as get_artefacts

import ssl_fix
from mattermost_api_client import get_user_by_email

import logging
logger = logging.getLogger(__name__)

c3_client_id = os.environ.get("C3_CLIENT_ID")
c3_client_secret = os.environ.get("C3_CLIENT_SECRET")

mattermost_token = os.environ.get("ERRBOT_TOKEN")
mattermost_base_url = f"https://{os.environ.get('ERRBOT_SERVER')}/api/v4"

if not c3_client_id or not c3_client_secret:
    raise Exception("C3_CLIENT_ID and C3_CLIENT_SECRET must be set")

C3_BASE_URL = 'https://certification.canonical.com'

c3_access_token = get_c3_access_token(C3_BASE_URL, c3_client_id, c3_client_secret)

now = datetime.now().date()

class CertificationPlugin(BotPlugin):
    """
    A plugin for interacting with Certification things
    """
    def __init__(self, bot, name):
        super().__init__(bot, name)
        self.user_cache = {}

    def get_assignee_handle(self, email):
        if email in self.user_cache:
            return self.user_cache[email]
        else:
            assignee_handle = get_user_by_email(mattermost_token, mattermost_base_url, email)
            self.user_cache[email] = assignee_handle
            return assignee_handle

    @botcmd(split_args_with=" ", name="cid")
    def cid(self, msg, args):
        c3_client = C3Client(base_url='https://certification.canonical.com', token=c3_access_token)

        # a command callable with !cid
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

    @botcmd(split_args_with=' ')
    def artefacts(self, msg, args):
        test_observer_client = TestObserverClient(base_url='https://test-observer-api.canonical.com')

        out_msg = ''
        artefacts_by_user = {}

        one_week_ago = now - timedelta(weeks=1)

        with test_observer_client:
            r = get_artefacts(client=test_observer_client)

            for artefact in r.parsed:
                if artefact.status == ArtefactStatus.APPROVED:
                    continue

                if artefact.status == ArtefactStatus.MARKED_AS_FAILED and artefact.due_date and artefact.due_date < one_week_ago:
                    continue

                assignee = artefact.assignee
                if not assignee and not artefact.due_date:
                    continue
                
                if assignee and assignee.launchpad_email:
                    assignee_handle = self.get_assignee_handle(assignee.launchpad_email)["username"]
                else:
                    assignee_handle = "No assignee"

                if args[0] == 'pending' and (artefact.status in [ArtefactStatus.MARKED_AS_FAILED]):
                    continue

                if assignee_handle not in artefacts_by_user:
                    artefacts_by_user[assignee_handle] = []

                artefacts_by_user[assignee_handle].append(artefact)

            if "all" in args:
                user_artefacts = artefacts_by_user
            else:
                sender_handle = msg.frm.username 
                if sender_handle in artefacts_by_user:
                    user_artefacts = {sender_handle: artefacts_by_user[sender_handle]}
                else:
                    user_artefacts = {}

            for user, artefacts in sorted(user_artefacts.items()):
                artefacts.sort(key=lambda x: (x.assignee is None,
                                               x.due_date is None,
                                               False if x.due_date is None else x.due_date < now,
                                               x.due_date or datetime.max.date()))
                if user == "No assignee":
                    out_msg += f"**{user}**\n"
                else:
                    out_msg += f"**@{user}**\n"
                for artefact in artefacts:
                    due_date_str = f" (due {artefact.due_date.strftime('%d-%m-%Y')})" if artefact.due_date else ""
                    completed_reviews = artefact.completed_environment_reviews_count
                    all_reviews = artefact.all_environment_reviews_count
                    review_percentage = round((completed_reviews / all_reviews) * 100) if all_reviews > 0 else 0
                    out_msg += f"- **[{artefact.name} {artefact.version}](https://test-observer.canonical.com/#/{artefact.repo}/{artefact.id})**: {artefact.status.lower()}{due_date_str} - {completed_reviews}/{all_reviews} reviews ({review_percentage:.0f}%)\n"
                out_msg += "\n"

            # Sort un-assigned artefacts last
            unassigned_artefacts = artefacts_by_user.pop("No assignee", [])
            if unassigned_artefacts:
                artefacts_by_user["No assignee"] = unassigned_artefacts

        return out_msg

