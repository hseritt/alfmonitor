""" Ping agent - checks up/down status of nodes."""
import socket
import psycopg2
from alfmonitor.lib.alflogger import logger
from agents.lib.abs_agent import AbstractConnectionAgent


socket.setdefaulttimeout(10)
DEFAULT_PORT = 5432


class PostgresqlAgent(AbstractConnectionAgent):

    agent_name = 'Postgresql'

    def __init__(self):
        self.log = logger(
            '{}.{}'.format(
                __name__,
                self.__class__.__name__,
            )
        )

    def connect(self, profile):
        """ Connects to profile's uri. """
        self.log.debug(f'Attempting db connection at {profile.uri}')

        is_connected = False

        host, db = profile.uri.split('/')
        try:
            hostname, port = host.split(':')
        except (IndexError, ValueError) as err:
            hostname = host
            port = DEFAULT_PORT

        try:
            connection = psycopg2.connect(
                host=hostname, user=profile.username, dbname=db,
                password=profile.password, port=int(port),
            )

            cursor = connection.cursor()

            if connection and cursor:
                is_connected = True

            cursor.close()
            connection.close()

        except psycopg2.OperationalError as err:
            self.log.debug(err)

        return is_connected


if __name__ == '__main__':
    agent = PostgresqlAgent()
    agent.run()
