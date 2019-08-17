import os
import sys
import django

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'alfmonitor.settings'
django.setup()

from agents.models import Agent
from add_agents import agent_list


def update_postgresql_agent():
    agent = Agent.objects.get(name='Postgresql', script='pg_agent')
    agent.script = 'postgresql_agent'
    agent.save()


def update_agent_script_names():
    print(
        '\nWARNING:\n\n'
        'If you have changed your script names from the default ones\n'
        'added at the first install of 0.0.2, you may need to manually\n'
        'change them to reflect the agent\'s class names.\n'
    )

    for agent in agent_list:
        a = Agent.objects.get(name=agent['name'])
        a.script = agent['script']
        a.save()


if __name__ == '__main__':
    update_postgresql_agent()
    update_agent_script_names()
