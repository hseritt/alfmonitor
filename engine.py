#!/usr/bin/env python
""" Engine to start up subsystems."""

import os
import sys
import time
import django

from threading import Thread

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'alfmonitor.settings'
django.setup()

from alfmonitor.lib.alflogger import logger
from agents.lib.subsystems import mailer
from agents.messages import SUBSYSTEM_STARTUP_MSG, SHUTDOWN_MSG
import monitor


LOGGER = logger(__name__)

subsystems = [
    monitor.AlfMonitorService,
    mailer.Mailer,
]


def run():
    for subsystem in subsystems:
        LOGGER.info(
            SUBSYSTEM_STARTUP_MSG.format(
                subsystem.__name__
            )
        )
        s = subsystem()
        thread = Thread(target=s.run)
        try:
            thread.start()
        except KeyboardInterrupt:
            LOGGER.info(SHUTDOWN_MSG)
            time.sleep(2)


if __name__ == '__main__':
    run()
