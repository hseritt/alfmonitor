""" Ping agent - checks up/down status of nodes."""
import socket
import requests
from alfmonitor.lib.alflogger import logger
from agents.lib.abs_agent import AbstractConnectionAgent


socket.setdefaulttimeout(10)


class HttpAgent(AbstractConnectionAgent):

    agent_name = 'Http'

    def __init__(self):
        self.log = logger(
            '{}.{}'.format(
                __name__,
                self.__class__.__name__,
            )
        )

    def connect(self, profile):
        """ Connects to profile's uri. """
        self.log.debug(f'  Attempting http GET at {profile.uri}')

        is_connected = False

        try:
            if profile.username and profile.password:
                response = requests.get(
                    profile.uri,
                    auth=(
                        profile.username, profile.password
                    )
                )
            else:
                response = requests.get(
                    profile.uri
                )
        except Exception as err:
            response = None

        if hasattr(response, 'status_code') and response.status_code == 200:
            is_connected = True

        return is_connected


if __name__ == '__main__':
    agent = HttpAgent()
    agent.run()
