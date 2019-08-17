#!/usr/bin/env python

import os
import requests
import zipfile

from django.utils import timezone
from alfmonitor.lib.alflogger import logger
from agents.messages import (
    RUN_AGENT_MSG, NO_PROFILE_CONFIGURED_MSG, MISSING_AGENT_MSG
)
from agents.models import Agent, Profile, JmxDumpData


jmxdump_path = '/alfresco/service/api/admin/jmxdump'
output_file = 'tmp/jmxdump.zip'


class JmxDumpAgent:

    agent_name = 'JMXDump'

    def __init__(self):

        self.log = logger(
            '{}.{}'.format(
                __name__,
                self.__class__.__name__,
            )
        )

    def download_jmxdump(self):
        response = requests.get(
            self.jmxdump_url,
            auth=(
                self.username, self.password
            )
        )

        open(output_file, 'wb').write(response.content)
        self.log.debug('ZipFile is {}'.format(output_file))
        zf = zipfile.ZipFile(output_file)
        zf.extractall('tmp')
        os.remove(output_file)

    def build_dict(self, profile):
        jmxdump_file = 'tmp/{}'.format(
            os.listdir('tmp')[0]
        )
        lines = open(jmxdump_file, 'r').readlines()
        out = '{\n'
        for line in lines:
            setting = line.split(' ')[0]
            value = line.split(' ')[-1].rstrip('\n')
            if '.' in setting and '=' not in setting:
                out += '    "{}" : "{}",\n'.format(
                    setting, value
                )
        out += '}\n'
        data = JmxDumpData()
        data.profile = profile
        data.event_time = timezone.now()
        data.content = out
        data.save()
        self.log.debug('Removing temp file: {}'.format(jmxdump_file))
        os.remove(jmxdump_file)

    def start(self, profile):
        self.profile = profile
        uri = profile.uri
        self.username = profile.username
        self.password = profile.password
        self.jmxdump_url = '{}{}'.format(uri, jmxdump_path)

        self.download_jmxdump()
        self.build_dict(self.profile)

    def run(self):
        self.log.debug(RUN_AGENT_MSG.format(self.agent_name))
        try:
            agent = Agent.objects.get(name=self.agent_name)
            profile_list = Profile.objects.filter(is_active=True, agent=agent)
            if not profile_list:
                self.log.info(
                    NO_PROFILE_CONFIGURED_MSG.format(self.agent_name)
                )
            for profile in profile_list:
                self.start(profile)
        except Agent.DoesNotExist as err:
            self.log.exception(
                MISSING_AGENT_MSG
            )
        self.log.handlers.pop()


if __name__ == '__main__':

    agent = JmxDumpAgent()
    agent.run()
