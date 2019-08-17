""" Test module for performance."""

import time
from alfmonitor.lib.alflogger import logger


LOGGER = logger(__name__)


def test_performance(start_time, profile, availability_test_passed):
    end_time = int(float(time.time() * 1000))
    total_time = end_time - start_time
    LOGGER.debug(
        f'Performance measured for {profile.name} is {total_time}ms.'
    )

    if availability_test_passed:
        if total_time < profile.performance_threshold:
            performance_test_passed = True
        else:
            performance_test_passed = False
    else:
        performance_test_passed = False
        total_time = -1

    LOGGER.debug(
        f'Performance test passed for '
        f'{profile.name} is '
        f'{performance_test_passed}.'
    )

    return performance_test_passed, total_time
