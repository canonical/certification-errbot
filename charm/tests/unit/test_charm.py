# Copyright 2025 Canonical
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from ops import testing

from charm import ErrbotCharm


class TestErrbotCharm(unittest.TestCase):
    def setUp(self):
        self.harness = testing.Harness(ErrbotCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_pebble_ready():
        # Arrange:
        ctx = testing.Context(ErrbotCharm)
        container = testing.Container("errbot", can_connect=True)
        state_in = testing.State(containers={container})

        # Act:
        state_out = ctx.run(ctx.on.pebble_ready(container), state_in)

        # Assert:
        assert state_out.unit_status == testing.ActiveStatus()
