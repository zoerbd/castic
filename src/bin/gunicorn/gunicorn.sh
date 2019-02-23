#!/bin/bash
cd /var/www/castic/src
/bin/pipenv run /usr/local/bin/gunicorn --pid /run/gunicorn/pid --bind unix:/run/gunicorn/socket castic.wsgi --workers 3
