#!/usr/bin/env python3
# Copyright 2025 Matias Piipari
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

"""Charm the service.

Refer to the following tutorial that will help you
develop a new k8s charm using the Operator Framework:

https://juju.is/docs/sdk/create-a-minimal-kubernetes-charm
"""

import logging
from typing import cast

import ops
from ops.model import BlockedStatus
from ops.pebble import ExecError, Layer

logger = logging.getLogger(__name__)
VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]


class CharmCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)
        framework.observe(self.on["errbot"].pebble_ready, self._on_errbot_pebble_ready)
        framework.observe(self.on.config_changed, self._on_config_changed)

    def _ensure_data_directory_exists(self, container):
        """Create a directory to contain the bot's transient state."""
        process = container.exec(["mkdir", "-p", "data"], working_dir="/app")

        try:
            stdout, _ = process.wait_output()
            logger.info(stdout)
        except ExecError as e:
            logger.error(e.stdout)
            logger.error(e.stderr)
            self.unit.status = BlockedStatus("Creating data directory failed")

    def _on_errbot_pebble_ready(self, event: ops.PebbleReadyEvent):
        container = event.workload
        self._ensure_data_directory_exists(container)

        container.add_layer("errbot", self._pebble_layer, combine=True)
        container.replan()
        self.unit.status = ops.ActiveStatus()

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        log_level = cast(str, self.model.config["log-level"]).lower()

        if log_level in VALID_LOG_LEVELS:
            container = self.unit.get_container("errbot")
            if container.can_connect():
                container.add_layer("errbot", self._pebble_layer, combine=True)
                container.replan()

                logger.debug("Log level set to '%s'", log_level)
                self.unit.status = ops.ActiveStatus()
            else:
                event.defer()
                self.unit.status = ops.WaitingStatus("waiting for Pebble API")
        else:
            self.unit.status = ops.BlockedStatus(f"invalid log level: '{log_level}'")

    @property
    def _pebble_layer(self) -> ops.pebble.LayerDict:
        return Layer(
            {
                "summary": "errbot layer",
                "description": "pebble config layer for errbot",
                "services": {
                    "errbot": {
                        "override": "replace",
                        "summary": "errbot",
                        "command": "errbot",
                        "startup": "enabled",
                        "environment": {
                            "ERRBOT_TOKEN": self.model.config["errbot-token"],
                            "ERRBOT_TEAM": self.model.config["errbot-team"],
                            "ERRBOT_SERVER": self.model.config["errbot-server"],
                            "ERRBOT_ADMINS": self.model.config["errbot-admins"],
                            "C3_CLIENT_ID": self.model.config["c3-client-id"],
                            "C3_CLIENT_SECRET": self.model.config["c3-client-secret"],
                        },
                    }
                },
            }
        )


if __name__ == "__main__":  # pragma: nocover
    ops.main(CharmCharm)  # type: ignore
