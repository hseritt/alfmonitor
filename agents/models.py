""" Models for agents app."""
from django.contrib.auth.models import User
from django.db import models
from alfmonitor.lib.alflogger import logger
from .field_choices import alarm_type_choices, protocol_choices


LOGGER = logger(__name__)


class Agent(models.Model):
    name = models.CharField('Name', max_length=50, unique=True)
    is_active = models.BooleanField('Is Active?', default=False)
    script = models.CharField('Script', max_length=50, unique=True)
    description = models.TextField('Description', null=True, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.PROTECT, help_text='*Required')
    name = models.CharField('Name', max_length=50, help_text='*Required')
    uri = models.CharField(
        'URI', max_length=1000,
        help_text='*Required Ex: localhost:22 or localhost:5432/mydb'
    )
    protocol = models.CharField(
        'Protocol', max_length=20, choices=(
            protocol_choices
        ),
        default='N/A',
        help_text='For Ping agent, default is TCP'
    )
    username = models.CharField(
        'Username', max_length=50, null=True, blank=True
    )
    password = models.CharField(
        'Password', max_length=50, null=True, blank=True
    )
    description = models.TextField('Description', null=True, blank=True)
    is_active = models.BooleanField('Is Active?', default=True)
    is_availability_checked = models.BooleanField(
        'Is Availability Checked?', default=True
    )
    is_performance_checked = models.BooleanField(
        'Is Performance Checked?', default=True
    )
    performance_threshold = models.IntegerField(
        'Performance Threshold in MS', null=True, blank=True, default=2000
    )
    is_alarm_created_for_availability = models.BooleanField(
        'Is Alarm Created for Availability Failure?',
        default=True,
    )
    is_alarm_created_for_performance = models.BooleanField(
        'Is Alarm Created for Performance Failure?',
        default=True,
    )
    is_data_stored_for_availability = models.BooleanField(
        'Is Data Stored for Availability?',
        default=True,
    )
    is_data_stored_for_performance = models.BooleanField(
        'Is Data Stored for Performance?',
        default=True,
    )
    admins = models.ManyToManyField(
        User, blank=True,
        help_text=(
            'Alert emails are sent to selected users. '
            'Use control or command (on Mac) to select multiple users.'
        )
    )

    class Meta:
        unique_together = (
            ('agent', 'name'),
        )

    def has_alarm(self):
        for alarm in Alarm.objects.filter(is_active=True):
            if self == alarm.profile and alarm.profile.is_active:
                return True
        return False

    def __str__(self):
        return f'{self.agent.name}: {self.name}'


class Data(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    is_availability_test_passed = models.BooleanField(
        'Is Availability Test Passed?',
    )

    # -2 not stored, -1 didn't test, 0 failed, 1 passed #
    is_performance_test_passed = models.IntegerField(
        'Is Performance Test Passed?',
        default='-2',
    )
    connect_time = models.IntegerField(null=True, blank=True)
    event_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-event_time', ]

    def __str__(self):
        out = f'{self.profile.agent.name} /' + \
            f'{self.profile.name} / {self.event_time}'
        return out


class JmxDumpData(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    event_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-event_time', ]

    def __str__(self):
        out = f'JmxDump Agent /' + \
            f'{self.profile.name} / {self.event_time}'
        return out


class Alarm(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    alarm_type = models.CharField(
        'Alarm Type', max_length=50, choices=(
            alarm_type_choices
        )
    )
    connect_time = models.IntegerField(null=True, blank=True)
    event_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField('Is Active?', default=True)

    def __str__(self):
        out = f'{self.profile.agent.name}: ' + \
            f'{self.profile.name} {self.alarm_type}' + \
            f' at {self.event_time}'
        return out
