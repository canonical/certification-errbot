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

    def test_dummy(self):
        assert True
