from errbot import BotPlugin, botcmd, re_botcmd
import os
from datetime import datetime

from c3.client import AuthenticatedClient as C3Client
from c3.api.physicalmachinesview.physicalmachinesview_list import sync_detailed as get_physicalmachinesview
from c3_auth import get_access_token as get_c3_access_token

import ssl_fix

import logging
logger = logging.getLogger(__name__)

from artefacts import reply_with_artefacts_summary, send_artefact_summaries

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

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
    
    def activate(self):
        super().activate()

        # Schedule the poller to run every weekday at 8:47 UTC
        scheduler = BackgroundScheduler()
        trigger = CronTrigger(day_of_week='mon-fri', hour=9, minute=00, timezone='UTC')
        scheduler.add_job(self.polled_digest_sending, trigger)
        scheduler.start()

    def polled_digest_sending(self):
        send_artefact_summaries(self)

    @botcmd(split_args_with=' ')
    def artefacts(self, msg, args):
        return reply_with_artefacts_summary(self, msg.frm, args)

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