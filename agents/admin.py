""" Admin settings for agents app."""
from django.contrib import admin
from .models import Agent, Alarm, Data, Profile, JmxDumpData


admin.site.register(Agent)
admin.site.register(Alarm)
admin.site.register(Data)
admin.site.register(JmxDumpData)
admin.site.register(Profile)
