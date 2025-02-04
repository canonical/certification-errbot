from errbot import BotPlugin, botcmd, re_botcmd
import re
import os
from c3.c3_client import C3ApiAgent

import ssl_fix


class CertificationPlugin(BotPlugin):
    """
    A plugin for interacting with Certification things
    """

    @botcmd(split_args_with=None)
    def cid(self, msg, args):
        # a command callable with !cid
        msg = ""

        client_id = os.environ.get("C3_CLIENT_ID")
        client_secret = os.environ.get("C3_CLIENT_SECRET")
        client = C3ApiAgent(client_id, client_secret)

        for cid in args:
            # test if the format is a CID

            # if it is contact c3 for summary of the machine

            msg += cid
            msg += "\n"

            r = client.get_physicalmachinesview(cid)
            msg = f"{r['make']} | {r['model']} | {r['tf_provision_type']}\n"

        return msg

    @re_botcmd(pattern=r"(^| )cookies?( |$)", prefixed=False, flags=re.IGNORECASE)
    def listen_for_talk_of_cookies(self, msg, match):
        """Talk of cookies gives Errbot a craving..."""
        return "Somebody mentioned cookies? Om nom nom!"
