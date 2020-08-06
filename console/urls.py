"""alfmonitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import login, logout
from django.urls import path
from alfmonitor.settings import VERSION
from .views import (
    index, agent, update_agent, profile, update_profile,
    profile_data, dashboard, alarms, profiles, add_profile
)

urlpatterns = [
    path('', index, name='console_index'),
    path('agent/<int:agent_id>/', agent, name='console_agent'),
    path(
        'agent/<int:agent_id>/update/',
        update_agent,
        name='console_update_agent'
    ),
    path(
        'alarms/', alarms, name='console_alarms',
    ),
    path('profile/<int:profile_id>/', profile, name='console_profile'),
    path('profile/add/', add_profile, name='console_add_profile'),
    path(
        'profile/<int:profile_id>/data/',
        profile_data,
        name='console_profile_data'
    ),
    path(
        'profile/<int:profile_id>/update/',
        update_profile,
        name='console_update_profile',
    ),
    path(
        'profiles/', profiles, name='console_profiles',
    ),
    path('dashboard/', dashboard, name='console_dashboard'),
    path(
        'login/',
        login,
        {
            'template_name': 'console/login.html',
            'extra_context': {
                'version': VERSION,
            },
        },
        name='login'
    ),
    path(
        'logout/',
        logout,
        {'next_page': '/console/login/?next=/'},
        name='logout'
    ),
]
