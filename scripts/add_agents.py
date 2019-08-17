#!/usr/bin/env python
""" Add agents in devsetup.sh."""

import os
import sys
import django

from django.db.utils import IntegrityError
sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'alfmonitor.settings'
django.setup()

from agents.models import Agent


agent_list = [
    {
        'name': 'Ping',
        'is_active': True,
        'script': 'agents.lib.ping_agent.PingAgent',
        'description': 'Tests up/down for network nodes.',
    },
    {
        'name': 'Http',
        'is_active': True,
        'script': 'agents.lib.http_agent.HttpAgent',
        'description': 'Tests availability and performance of HTTP URLs.',
    },
    {
        'name': 'Postgresql',
        'is_active': True,
        'script': 'agents.lib.postgresql_agent.PostgresqlAgent',
        'description': (
            'Tests availability and performance of Postgresql connections.'
        ),
    },
    {
        'name': 'CMIS Rest API',
        'is_active': True,
        'script': 'agents.lib.cmis_rest_agent.CmisRestAgent',
        'description': (
            'Tests availability and performance of Alfresco '
            'CMIS Rest API endpoints.'
        ),
    },
    {
        'name': 'JMXDump',
        'is_active': True,
        'script': 'agents.lib.jmxdump_agent.JmxDumpAgent',
        'description': (
            'Stores all settings of a running Alfresco system '
            'for archival purposes.'
        ),
    },
]


if __name__ == '__main__':

    for agent in agent_list:
        a = Agent()
        for k, v in agent.items():
            setattr(a, k, v)
        try:
            a.save()
        except IntegrityError:
            print('Agent already exists.')
