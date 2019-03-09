#!/usr/bin/env python3
import os, sys
sys.path.insert(0, '/var/www/castic/src/') # insert path to import project-stuff (make more dynamic later on)

from django.conf import settings
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "castic.settings")
setup()
from update.check import checkRepositories

help = "This command is mainly called from cron update automation."
checkRepositories()
