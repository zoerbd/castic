# ------------------------------------------------------------>
# ---- Globally used config-vars and function defined here ---

import json, subprocess
from django.shortcuts import redirect
from django.utils.timezone import now

# read config file
with open('../config.json') as jsonFile:
        config = json.load(jsonFile)

def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        return subprocess.check_output(command, shell=True).decode('utf-8').strip()
       
def __log__(msg):
    # if empty argument given, no error occurred
    if not msg:
        return

    # document and return
    print(msg)
    with open('castic.log', 'a') as logfile:
        logfile.write('{} - {}'.format(now(), msg))
    return msg

def loginRequired(func):
    '''
    Basic decorator to apply on views to require user to be logged in.
    '''
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return redirect('/login')
        return func(*args, **kwargs)
    return wrapper

def getVersion():
    '''
    Returns current version.
    '''
    return '0.6.2'
# ------------------------------------------------------------>
