""" Data handler module."""
from agents.models import Data
from alfmonitor.lib.alflogger import logger


LOGGER = logger(__name__)


def store_data(
    profile, availability_test_passed, performance_test_passed,
    total_time, event_time
):
    data = Data()
    data.profile = profile
    data.is_availability_test_passed = availability_test_passed
    data.event_time = event_time

    if profile.is_data_stored_for_performance:
        data.is_performance_test_passed = performance_test_passed
        data.connect_time = total_time
    LOGGER.debug('Saving data from profile: {}'.format(profile.name))
    data.save()
