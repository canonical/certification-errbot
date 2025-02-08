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

from test_observer.api.artefacts.get_artefacts_v1_artefacts_get import sync_detailed as get_artefacts
from types import UserLike

import ssl_fix

import logging
logger = logging.getLogger(__name__)

from artefacts import artefacts_summary

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
        self.start_poller(1, self.poll_for_artefacts)

    def poll_for_artefacts(self):
        msg = artefacts_summary(self, "mz2", args)
        self.log.debug(msg)


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
        return artefacts_summary(self, msg.frm, args)
