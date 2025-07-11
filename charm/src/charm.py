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
from ops.pebble import LayerDict, ServiceDict

logger = logging.getLogger(__name__)
VALID_LOG_LEVELS = ["info", "debug", "warning", "error", "critical"]


class ErrbotCharm(ops.CharmBase):
    """Charm the service."""

    def __init__(self, framework: ops.Framework):
        super().__init__(framework)
        framework.observe(self.on["errbot"].pebble_ready, self._on_errbot_pebble_ready)
        framework.observe(self.on.config_changed, self._on_config_changed)

    def _on_errbot_pebble_ready(self, event: ops.PebbleReadyEvent):
        container = event.workload
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
        return LayerDict(
            summary="errbot layer",
            description="pebble config layer for errbot",
            services={
                "errbot": ServiceDict(
                    override="replace",
                    summary="errbot",
                    command="errbot",
                    startup="enabled",
                    environment={
                        "C3_CLIENT_ID": str(self.model.config["c3-client-id"]),
                        "C3_CLIENT_SECRET": str(self.model.config["c3-client-secret"]),
                        "DIGEST_SEND_TIME": str(self.model.config["digest-send-time"]),
                        "ERRBOT_ADMINS": str(self.model.config["mattermost-admins"]),
                        "ERRBOT_SERVER": str(self.model.config["mattermost-server"]),
                        "ERRBOT_TEAM": str(self.model.config["mattermost-team"]),
                        "ERRBOT_TOKEN": str(self.model.config["mattermost-token"]),
                        "GITHUB_ORG": str(self.model.config["github-org"]),
                        "GITHUB_REPOSITORIES": str(self.model.config["github-repositories"]),
                        "GITHUB_TEAM": str(self.model.config["github-team"]),
                        "GITHUB_TOKEN": str(self.model.config["github-token"]),
                        "HTTPS_PROXY": str(self.model.config["https-proxy"]),
                        "HTTP_PROXY": str(self.model.config["http-proxy"]),
                        "JIRA_CURRENT_SPRINT_ONLY": str(
                            self.model.config["jira-current-sprint-only"]
                        ).lower(),
                        "JIRA_EMAIL": str(self.model.config["jira-email"]),
                        "JIRA_FILTER_ID": str(self.model.config["jira-filter-id"]),
                        "JIRA_SERVER": str(self.model.config["jira-server"]),
                        "JIRA_TOKEN": str(self.model.config["jira-token"]),
                        "LDAP_BASE_DN": str(self.model.config["ldap-base-dn"]),
                        "LDAP_BIND_DN": str(self.model.config["ldap-bind-dn"]),
                        "LDAP_BIND_PASSWORD": str(self.model.config["ldap-bind-password"]),
                        "LDAP_SERVER": str(self.model.config["ldap-server"]),
                        "NO_PROXY": str(self.model.config["no-proxy"]),
                    },
                ),
            },
        )


if __name__ == "__main__":  # pragma: nocover
    ops.main(ErrbotCharm)  # type: ignore
