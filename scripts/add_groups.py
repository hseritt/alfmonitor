#!/usr/bin/env python

import os
import sys
import django

from django.db.utils import IntegrityError

sys.path.append('.')
os.environ['DJANGO_SETTINGS_MODULE'] = 'alfmonitor.settings'
django.setup()

from django.contrib.auth.models import Group, User


user_groups = (
    'console_admins',
    'console_users',
)


if __name__ == '__main__':
    admin_user = User.objects.get(username='admin')

    for group_name in user_groups:
        group = Group()
        group.name = group_name
        try:
            group.save()
        except IntegrityError:
            print('Group: {} alfready exists.'.format(group_name))

    admin_user.groups.add(Group.objects.get(name='console_admins'))
