#!/usr/bin/env python3
"""
Tests for plugins/certification/mattermost_keepalive.py

Covers:
  - enable_mattermost_websocket_keepalive sets Driver.default_options["keepalive"] = True
  - it is idempotent (safe to call repeatedly)
  - it does not clobber other existing default_options entries
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mattermostdriver.driver import Driver

from plugins.certification.mattermost_keepalive import (
    enable_mattermost_websocket_keepalive,
)


class TestMattermostKeepalive(unittest.TestCase):
    def setUp(self):
        # Snapshot so tests don't leak state into each other or other test
        # modules that import mattermostdriver.
        self._original_default_options = Driver.default_options.copy()

    def tearDown(self):
        Driver.default_options.clear()
        Driver.default_options.update(self._original_default_options)

    def test_enables_keepalive(self):
        Driver.default_options["keepalive"] = False
        enable_mattermost_websocket_keepalive()
        self.assertTrue(Driver.default_options["keepalive"])

    def test_idempotent(self):
        enable_mattermost_websocket_keepalive()
        enable_mattermost_websocket_keepalive()
        self.assertTrue(Driver.default_options["keepalive"])

    def test_does_not_clobber_other_defaults(self):
        before = Driver.default_options.copy()
        enable_mattermost_websocket_keepalive()
        after = Driver.default_options
        for key, value in before.items():
            if key == "keepalive":
                continue
            self.assertEqual(after[key], value)

    def test_new_driver_instance_picks_up_keepalive(self):
        enable_mattermost_websocket_keepalive()
        driver = Driver()
        self.assertTrue(driver.options["keepalive"])


if __name__ == "__main__":
    unittest.main()
