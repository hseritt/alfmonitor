""" Test module for availability."""

import time
from django.utils import timezone
from alfmonitor.lib.alflogger import logger
from agents.lib.tests.performance_test import test_performance

LOGGER = logger(__name__)


def test_availability(profile, connect):
    if profile.is_performance_checked:
            start_time = int(float(time.time() * 1000))

    event_time = timezone.now()
    availability_test_passed = connect(profile)

    if profile.is_performance_checked:
        performance_test_passed, total_time = test_performance(
            start_time, profile, availability_test_passed
        )

    LOGGER.debug(
        f'Availability test passed for '
        f'{profile.name} is '
        f'{availability_test_passed}.'
    )

    return (
        availability_test_passed,
        performance_test_passed,
        total_time, event_time
    )
