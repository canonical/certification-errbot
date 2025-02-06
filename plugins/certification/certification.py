from errbot import BotPlugin, botcmd, re_botcmd
import re
import os

from c3.client import AuthenticatedClient as C3Client
from c3.api.physicalmachinesview.physicalmachinesview_list import sync_detailed as get_physicalmachinesview
from c3.models import PhysicalMachineView
from c3.types import Response
from c3_auth import get_access_token as get_c3_access_token

from test_observer.models import ArtefactDTO
from test_observer.client import Client as TestObserverClient
from test_observer.api.artefacts.get_artefacts_v1_artefacts_get import sync_detailed as get_artefacts

import ssl_fix

c3_client_id = os.environ.get("C3_CLIENT_ID")
c3_client_secret = os.environ.get("C3_CLIENT_SECRET")


if not c3_client_id or not c3_client_secret:
    raise Exception("C3_CLIENT_ID and C3_CLIENT_SECRET must be set")

C3_BASE_URL = 'https://certification.canonical.com'

c3_access_token = get_c3_access_token(C3_BASE_URL, c3_client_id, c3_client_secret)
c3_client = C3Client(base_url='https://certification.canonical.com', token=c3_access_token)

test_observer_client = TestObserverClient(base_url='https://test-observer-api.canonical.com')

class CertificationPlugin(BotPlugin):
    """
    A plugin for interacting with Certification things
    """

    @botcmd(split_args_with=" ", name="cid")
    def cid(self, msg, args):
        # a command callable with !cid
        msg = ""

        with c3_client:
            for cid in args:
                # test if the format is a CID

                # if it is contact c3 for summary of the machine

                msg += cid
                msg += "\n"

                r = get_physicalmachinesview(client=c3_client, canonical_id=cid)

                for machine in r.parsed:
                    make = machine.make if r.make is not None else "Unknown"
                    model = machine.model if r.model is not None else "Unknown"
                    tf_provision_type = machine.tf_provision_type if machine.tf_provision_type is not None else "Unknown"

                    msg = f"{make} | {model} | {tf_provision_type}\n"

            return msg

    @botcmd(split_args_with=None)
    def artefacts(self, msg, args):
        msg = ''

        with test_observer_client:
            r = get_artefacts(client=test_observer_client)

            for artefact in r.parsed:
                msg += f"{artefact.name} | {artefact.version} | {artefact.status}\n"
            

        return msg

