"""Patch mattermostdriver to automatically reconnect its websocket.

``err-backend-mattermost``'s ``serve_once()`` constructs a ``mattermostdriver.Driver``
with a fixed whitelist of options that does not include ``keepalive``, so the
driver silently falls back to its own default of ``keepalive=False``.

With ``keepalive=False``, ``mattermostdriver.websocket.Websocket.connect()``
*returns* (rather than raising) the first time the websocket disconnects --
whether from a ping-timeout, a Mattermost server restart, or an idle
connection being silently dropped by an intermediate egress proxy. Because
``serve_once()`` drives that coroutine via ``loop.run_until_complete(...)``
and then calls ``loop.run_forever()``, the asyncio loop is left spinning with
nothing scheduled: no exception is raised, no reconnect is attempted, and no
error is logged. The bot still looks healthy (REST calls / cron jobs keep
working) but silently stops receiving any new Mattermost events until the
whole process is restarted.

Patching the class-level default here -- before any ``Driver`` is
constructed -- causes mattermostdriver's own reconnect loop
(``Websocket.connect()``'s outer ``while True``) to keep retrying on any
disconnection instead of giving up after the first one.
"""

import logging

from mattermostdriver.driver import Driver

logger = logging.getLogger(__name__)


def enable_mattermost_websocket_keepalive() -> None:
    """Enable automatic websocket reconnection for all future Driver instances.

    Safe to call multiple times (idempotent) and must run before
    ``err-backend-mattermost`` constructs its ``Driver`` (i.e. before the bot
    connects to Mattermost), so it should be invoked as early as possible --
    e.g. from ``config.py``, which errbot loads before starting the backend.
    """
    if Driver.default_options.get("keepalive") is True:
        return
    Driver.default_options["keepalive"] = True
    logger.info(
        "Patched mattermostdriver.Driver.default_options: keepalive=True "
        "(enables automatic websocket reconnection on disconnect)"
    )
