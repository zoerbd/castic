#!/bin/bash
cd /var/www/castic/src 
gunicorn --pid /run/gunicorn/pid --bind unix:/run/gunicorn/socket castic.wsgi --workers 3 -k 'eventlet'
