#!/usr/bin/env python
""" Modify admin user's password during devsetup.sh."""
import os
import sys

sys.path.append('.')
sys.path.append('..')

os.environ['DJANGO_SETTINGS_MODULE'] = 'alfmonitor.settings'

import django

django.setup()

from django.contrib.auth.models import User


if __name__ == '__main__':
    admin_user = User.objects.get(username='admin')
    admin_user.set_password('admin')
    try:
        admin_user.email = os.environ['DJANGO_ADMIN_EMAIL']
    except KeyError:
        pass
    admin_user.save()
