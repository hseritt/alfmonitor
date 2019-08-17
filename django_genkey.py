#!/usr/bin/env python

from django.core.management import utils

secret_key = utils.get_random_secret_key()

content = open('alfmonitor/settings-dist.py').readlines()

out = ''

for line in content:
	if 'SECRET_KEY' in line:
		line = "SECRET_KEY = '{}'\n".format(secret_key)

	out += line

open('alfmonitor/settings-dist.py', 'w').write(out)
