#!/usr/bin/env python
""" Main alfmonitor server engine."""


import datetime
import importlib
import os
import sys
import time

import django

sys.path.append('.')
sys.path.append('..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'alfmonitor.settings'
django.setup()

from alfmonitor.settings import AGENT_RUN_FREQUENCY
from agents.messages import (
    SVC_START_MSG, ACTVE_AGENTS_MSG, INACTIVE_MAIL_MSG,
    START_AGENT_MSG, ENGINE_SLEEP_MSG, SCRIPT_CALL_MSG
)
from agents.models import Agent
from alfmonitor.lib.alflogger import logger


LOGGER = logger(__name__)


def get_mod_and_class(script):
    return (
        '.'.join(script.split('.')[:-1]),
        script.split('.')[-1]
    )


class AlfMonitorService(object):

    def run(self):
        """ Runs the Alfmonitor engine."""
        LOGGER.info(
            SVC_START_MSG.format(
                datetime.datetime.now()
            )
        )

        LOGGER.info('Running active agents.')

        while True:
            active_agent_list = Agent.objects.filter(is_active=True)
            LOGGER.debug(
                ACTVE_AGENTS_MSG.format(
                    ', '.join(
                        [agent.name for agent in active_agent_list]
                    )
                )
            )

            try:
                mail_agent = Agent.objects.get(name='Mail')
                if mail_agent not in active_agent_list:
                    LOGGER.info(
                        INACTIVE_MAIL_MSG
                    )
            except Agent.DoesNotExist:
                pass

            for agent in active_agent_list:
                LOGGER.debug(START_AGENT_MSG.format(agent.name))

                try:
                    module, class_name = get_mod_and_class(agent.script)
                    LOGGER.debug('Agent module: {}'.format(module))
                    LOGGER.debug('Agent class: {}'.format(class_name))
                    AgentClass = getattr(
                        importlib.import_module(module),
                        class_name
                    )
                    agent = AgentClass()
                    agent.run()

                except ModuleNotFoundError as err:
                    LOGGER.exception(
                        "Check for misspelling of the agent's script name.\n"
                        f"Agent > name: {agent.name} |"
                        f" script: {agent.script}\n"
                    )

            LOGGER.debug(
                ENGINE_SLEEP_MSG.format(AGENT_RUN_FREQUENCY)
            )
            time.sleep(AGENT_RUN_FREQUENCY)


if __name__ == '__main__':
    print(SCRIPT_CALL_MSG)
    print('Exiting.')
    sys.exit(0)

    LOGGER.info("Starting up AlfMonitor Server.")
    server = AlfMonitorService()
    server.run()
