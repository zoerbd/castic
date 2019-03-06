#!/usr/bin/env python3
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "castic.settings")


if __name__ == "__main__":
    args = sys.argv
    args.insert(1, "test")
    args.insert(2, "--noinput")

    from castic.settings import INSTALLED_APPS
    from django.core.management import execute_from_command_line
    [args.append(app) for app in INSTALLED_APPS]
    execute_from_command_line(args)