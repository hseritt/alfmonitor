""" Forms module for agents app."""
from django.forms import ModelForm
from agents.models import Agent, Profile


class UpdateAgentForm(ModelForm):

    class Meta:
        model = Agent
        fields = ['is_active', 'script', 'description', ]


class UpdateProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = [
            'name', 'uri', 'description', 'protocol', 'username',
            'is_active', 'is_availability_checked', 'is_performance_checked',
            'performance_threshold', 'is_alarm_created_for_availability',
            'is_alarm_created_for_performance',
            'is_data_stored_for_availability',
            'is_data_stored_for_performance',
        ]


class AddProfileForm(ModelForm):

    class Meta:
        model = Profile
        fields = [
            'agent', 'name', 'uri', 'description', 'protocol', 'username',
            'password', 'is_active', 'is_availability_checked',
            'is_performance_checked', 'performance_threshold',
            'is_alarm_created_for_availability',
            'is_alarm_created_for_performance',
            'is_data_stored_for_availability',
            'is_data_stored_for_performance', 'admins',
        ]
