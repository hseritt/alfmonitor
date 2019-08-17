""" CMIS Rest API agent."""
import socket
import requests
from alfmonitor.lib.alflogger import logger
from agents.lib.abs_agent import AbstractConnectionAgent


socket.setdefaulttimeout(10)


class CmisRestAgent(AbstractConnectionAgent):

    agent_name = 'CMIS Rest API'

    def __init__(self):
        self.log = logger(
            '{}.{}'.format(
                __name__,
                self.__class__.__name__,
            )
        )

    def connect(self, profile):
        self.log.debug(f'  Attempting http GET at {profile.uri}')
        is_connected = False

        try:
            response = requests.get(
                profile.uri,
                auth=(
                    profile.username,
                    profile.password,
                ),
            )
        except Exception as err:
            self.log.error(repr(err))
            response = None

        if hasattr(response, 'status_code') and response.status_code == 200:
            is_connected = True

        return is_connected


if __name__ == '__main__':
    agent = CmisRestAgent()
    agent.run()
