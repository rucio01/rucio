# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Luis Rodrigues, <luis.rodrigues@cern.ch>, 2013

from rucio.core import monitor


class TestMonitor():

    @classmethod
    def setupClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_monitor_record_message(self):
        """MONITOR (CORE): Send a message to graphite """
        monitor.record('test.stuff', 10)

    def test_monitor_gaude_message(self):
        """MONITOR (CORE): Send a message to graphite """
        monitor.gauge('test.gauge', 10)

    def test_monitor_timing_message(self):
        """MONITOR (CORE): Send a message to graphite """
        monitor.timing('test.runtime', 500)
