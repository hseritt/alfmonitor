""" Ping agent - checks up/down status of nodes."""
import socket
from alfmonitor.lib.alflogger import logger
from agents.lib.abs_agent import AbstractConnectionAgent


socket.setdefaulttimeout(10)


class PingAgent(AbstractConnectionAgent):

    agent_name = 'Ping'

    def __init__(self):
        self.log = logger(
            '{}.{}'.format(
                __name__,
                self.__class__.__name__,
            )
        )

    def connect(self, profile):
        """ Connects to profile's uri. """
        try:
            hostname, port = profile.uri.split(':')
        except (IndexError, ValueError) as err:
            hostname = profile.uri
            port = 0
            self.log.exception(err)
            self.log.error('Port cannot be assigned. Attempting with port 0.')

        self.log.debug(
            f'Attempting connection to {hostname} '
            f'at port {port} ...'
        )

        if profile.protocol == 'TCP':
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif profile.protocol == 'UDP':
            connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        else:
            self.log.warn(
                f'Protocol not set for profile: {profile.name}. Assuming TCP.'
            )
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        address = (hostname, int(port))
        is_connected = False

        try:
            connection.connect(address)
            is_connected = True
        except (socket.timeout, ConnectionRefusedError):
            pass
        except socket.gaierror as err:
            self.log.exception(
                'Check to see if this profile should use Http agent instead '
                'of Ping agent.\n'
                f'Profile uri is {profile.uri}'
            )
        finally:
            connection.close()

        return is_connected


if __name__ == '__main__':
    agent = PingAgent()
    agent.run()
