"""Views module for the console app."""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from alfmonitor.settings import (
    AGENT_RUN_FREQUENCY, VERSION
)
from agents.models import Agent, Alarm, Data, Profile
from .forms import UpdateAgentForm, UpdateProfileForm, AddProfileForm
import console.messages as msg
from alfmonitor.lib.alflogger import logger


LOGGER = logger(__name__)

agent_run_frequency = AGENT_RUN_FREQUENCY * 1000


def in_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


def in_console_admins_group(user):
    return in_group(user, 'console_admins')


def messages_context():
    context = {
        'agents_header': msg.AGENTS_HEADER,
        'active_profiles_header': msg.ACTIVE_PROFILES_HEADER,
        'active_alarms_header': msg.ACTIVE_ALARMS_HEADER,
        'dashboard_header': msg.DASHBOARD_HEADER,
        'last_inactive_alarms': msg.LAST_INACTIVE_ALARMS,
        'no_active_alarms_msg': msg.NO_ACTIVE_ALARMS_MSG,
        'no_profiles_configured_msg': msg.NO_PROFILES_CONFIGURED_MSG,
        'setup_profile_header': msg.SETUP_PROFILE_HEADER,
    }
    return context


def navigation_context():
    agent_list = Agent.objects.all()
    profile_list = Profile.objects.filter(is_active=True).order_by('name')
    context = {
        'agent_list': agent_list,
        'profile_list': profile_list,
        'version': VERSION,
    }

    context.update(messages_context())
    return context


def root_index(request):
    return HttpResponseRedirect('/console/')


@login_required(login_url='/console/login/')
def index(request):
    alarm_list = Alarm.objects.filter(is_active=True, profile__is_active=True)
    inactive_alarm_list = Alarm.objects.filter(is_active=False)[:20]

    view_context = {
        'agent_run_frequency': agent_run_frequency,
        'alarm_list': alarm_list,
        'inactive_alarm_list': inactive_alarm_list,
        'refresh_page': True,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/index.html',
        view_context,
    )


@login_required(login_url='/console/login/')
def agent(request, agent_id):
    agent = Agent.objects.get(pk=agent_id)
    assoc_profile_list = Profile.objects.filter(agent=agent).order_by('name')

    view_context = {
        'agent': agent,
        'assoc_profile_list': assoc_profile_list,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/agent.html',
        view_context
    )


@login_required(login_url='/console/login/')
@user_passes_test(in_console_admins_group, login_url='/console/login/')
def update_agent(request, agent_id):
    agent = Agent.objects.get(pk=agent_id)

    if request.method == 'GET':
        update_agent_form = UpdateAgentForm(instance=agent)

    if request.method == 'POST':
        update_agent_form = UpdateAgentForm(request.POST, instance=agent)

        if update_agent_form.is_valid():
            update_agent_form.save()

        return HttpResponseRedirect(reverse('console_agent', args=(agent.id,)))

    view_context = {
        'agent': agent,
        'update_agent_form': update_agent_form,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/update_agent.html',
        view_context,
    )


@login_required(login_url='/console/login/')
def profile(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)

    view_context = {
        'profile': profile,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/profile.html',
        view_context,
    )


@login_required(login_url='/console/login/')
@user_passes_test(in_console_admins_group, login_url='/console/login/')
def update_profile(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)

    if 'next' in request.GET:
        next_url = request.GET.get('next')
    else:
        next_url = None

    if request.method == 'GET':
        update_profile_form = UpdateProfileForm(instance=profile)

    if request.method == 'POST':
        update_profile_form = UpdateProfileForm(request.POST, instance=profile)

        if update_profile_form.is_valid():
            update_profile_form.save()

        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return HttpResponseRedirect(
                reverse(
                    'console_profile', args=(profile.id,)
                )
            )

    view_context = {
        'agent': agent,
        'profile': profile,
        'update_profile_form': update_profile_form,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/update_profile.html',
        view_context,
    )


@login_required(login_url='/console/login/')
def profile_data(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)

    data_list = Data.objects.filter(profile=profile)

    paginator = Paginator(data_list, 100)
    page = request.GET.get('page', 1)
    data = paginator.get_page(page)

    view_context = {
        'agent_run_frequency': agent_run_frequency,
        'profile': profile,
        'data': data,
        'refresh_page': True,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/profile_data.html',
        view_context,
    )


@login_required(login_url='/console/login/')
def dashboard(request):
    alarm_list = Alarm.objects.filter(is_active=True)

    view_context = {
        'agent_run_frequency': agent_run_frequency,
        'alarm_list': alarm_list,
        'refresh_page': True,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/dashboard.html',
        view_context,
    )


@login_required(login_url='/console/login/')
def alarms(request):
    alarm_list = Alarm.objects.all().order_by('-event_time')

    paginator = Paginator(alarm_list, 50)
    page = request.GET.get('page', 1)
    alarms = paginator.get_page(page)

    view_context = {
        'alarms': alarms,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/alarms.html',
        view_context,
    )


@login_required(login_url='/console/login/')
def profiles(request):
    active_profile_list = Profile.objects.filter(
        is_active=True
    ).order_by('name')

    inactive_profile_list = Profile.objects.filter(
        is_active=False
    ).order_by('name')

    view_context = {
        'active_profile_list': active_profile_list,
        'inactive_profile_list': inactive_profile_list,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/profiles.html',
        view_context,
    )


@login_required(login_url='/console/login/')
@user_passes_test(in_console_admins_group, login_url='/console/login/')
def add_profile(request):
    if request.method == 'GET':
        add_profile_form = AddProfileForm()

    if request.method == 'POST':
        add_profile_form = AddProfileForm(request.POST)
        if add_profile_form.is_valid():
            add_profile_form.save()
            return HttpResponseRedirect('/console/')

    view_context = {
        'add_profile_form': add_profile_form,
    }
    view_context.update(navigation_context())

    return render(
        request,
        'console/add_profile.html',
        view_context,
    )
