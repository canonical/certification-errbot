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

logger = logging.getLogger(__name__)
VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]


class CharmCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)
        framework.observe(self.on["errbot"].pebble_ready, self._on_errbot_pebble_ready)
        framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_errbot_pebble_ready(self, event: ops.PebbleReadyEvent):
        """Define and start a workload using the Pebble API.

        Change this example to suit your needs. You'll need to specify the right entrypoint and
        environment configuration for your specific workload.

        Learn more about interacting with Pebble at at https://juju.is/docs/sdk/pebble.
        """
        container = event.workload
        container.add_layer("errbot", self._pebble_layer, combine=True)
        container.replan()
        self.unit.status = ops.ActiveStatus()

    def _on_config_changed(self, event: ops.ConfigChangedEvent):
        """Handle changed configuration.

        Change this example to suit your needs. If you don't need to handle config, you can remove
        this method.

        Learn more about config at https://juju.is/docs/sdk/config
        """
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
        """Return a dictionary representing a Pebble layer."""
        return {
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


if __name__ == "__main__":  # pragma: nocover
    ops.main(CharmCharm)  # type: ignore
