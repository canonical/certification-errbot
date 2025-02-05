from errbot import BotPlugin, botcmd, re_botcmd
import re
import os
from c3.c3_client import C3ApiAgent
from test_observer.models import ArtefactDTO
from test_observer.client import Client
from test_observer.api.artefacts import get_artefacts_v1_artefacts_get

import ssl_fix

c3_client_id = os.environ.get("C3_CLIENT_ID")
c3_client_secret = os.environ.get("C3_CLIENT_SECRET")

if c3_client_id is None or c3_client_secret is None:
    raise Exception("C3_CLIENT_ID and C3_CLIENT_SECRET must be set")

c3_client = C3ApiAgent(c3_client_id, c3_client_secret)


class CertificationPlugin(BotPlugin):
    """
    A plugin for interacting with Certification things
    """

    @botcmd(split_args_with=None)
    def cid(self, msg, args):
        # a command callable with !cid
        msg = ""

        for cid in args:
            # test if the format is a CID

            # if it is contact c3 for summary of the machine

            msg += cid
            msg += "\n"

            r = c3_client.get_physicalmachinesview(cid)
            msg = f"{r['make']} | {r['model']} | {r['tf_provision_type']}\n"

        return msg

    @botcmd(split_args_with=None)
    def artefacts(self, msg, args):
        msg = ""
