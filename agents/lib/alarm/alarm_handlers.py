""" Alarm handler module."""

from django.utils import timezone
from agents.models import Alarm


def add_alarm(profile, alarm_type, test):
    try:
        existing_alarm = Alarm.objects.get(
            profile=profile, is_active=True,
            alarm_type=alarm_type
        )
    except Alarm.DoesNotExist:
        existing_alarm = None

    if not test:

        if existing_alarm:
            pass
        else:
            alarm = Alarm()
            alarm.profile = profile
            alarm.event_time = timezone.now()
            alarm.alarm_type = alarm_type
            alarm.save()

    else:
        if existing_alarm:
            existing_alarm.is_active = False
            existing_alarm.save()


def add_availability_alarm(profile, availability_test_passed):
    add_alarm(
        profile, 'Availability Failure', availability_test_passed
    )


def add_performance_alarm(profile, performance_test_passed, total_time):
    add_alarm(
        profile, 'Performance Failure', performance_test_passed
    )
