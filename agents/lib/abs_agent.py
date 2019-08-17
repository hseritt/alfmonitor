
from agents.lib.alarm.alarm_handlers import (
    add_availability_alarm, add_performance_alarm
)
from agents.lib.data.data_handlers import store_data
from agents.lib.tests.availability_test import test_availability
from agents.messages import (
    RUN_AGENT_MSG, NO_PROFILE_CONFIGURED_MSG, MISSING_AGENT_MSG
)
from agents.models import Agent, Profile


class AbstractConnectionAgent:

    agent_name = 'Abstract Agent'

    def test(self, profile):
        """ Tests profile. """
        self.log.debug(f'Testing profile: {profile.name}')
        availability_test_passed = False

        total_time = -1

        if profile.is_availability_checked:
            (
                availability_test_passed, performance_test_passed,
                total_time, event_time
            ) = test_availability(profile, self.connect)

        if profile.is_data_stored_for_availability:
            store_data(
                profile, availability_test_passed, performance_test_passed,
                total_time, event_time
            )

        if profile.is_alarm_created_for_availability:
            add_availability_alarm(
                profile,
                availability_test_passed
            )

        if profile.is_alarm_created_for_performance:
            add_performance_alarm(
                profile,
                performance_test_passed,
                total_time
            )

    def run(self):
        """ Runs this agent."""
        self.log.debug(RUN_AGENT_MSG.format(self.agent_name))
        try:
            agent = Agent.objects.get(name=self.agent_name)
            profile_list = Profile.objects.filter(is_active=True, agent=agent)
            if not profile_list:
                self.log.info(
                    NO_PROFILE_CONFIGURED_MSG.format(self.agent_name)
                )
            for profile in profile_list:
                self.test(profile)
        except Agent.DoesNotExist as err:
            self.log.exception(
                MISSING_AGENT_MSG
            )
        self.log.handlers.pop()
