from errbot import BotPlugin, botcmd, re_botcmd
import re
import os
from lib.fast_api_client import Client

import ssl_fix


class TestObserver(BotPlugin):
    """
    A plugin for interacting with Test Observer
    """

    @botcmd(split_args_with=None)
    def cid(self, msg, args):
        # a command callable with !cid
        msg = ""

        base_uri = os.environ.get(
            "TEST_OBSERVER_API_BASE_URI", "https://test-observer-api.canonical.com"
        )
        client = Client(base_url=base_uri, follow_redirects=True)

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
