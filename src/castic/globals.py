# ------------------------------------------------------------>
# ---- Globally used config-vars and function defined here ---

import json, subprocess, os, sys
sys.path.insert(0, '/var/www/castic/src')
from django.shortcuts import redirect
from django.utils.timezone import now
from castic.settings import BASE_DIR

# read config file
gitProjectDir = '/'.join(BASE_DIR.split('/')[:-1])   # get parent dir of src
with open(os.path.join(gitProjectDir, 'config.json')) as jsonFile:
        config = json.load(jsonFile)

def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        process = subprocess.Popen(command.split(' '), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = [ item.decode('utf-8').strip() for item in process.communicate()]
        if not stderr:
            return stdout
        return __log__("Shell command failed with: {}".format(stderr))
       
def __log__(msg):
    # if empty argument given, no error occurred
    if not msg:
        return

    # document and return
    print(msg)
    with open(os.path.join(gitProjectDir, 'castic.log'), 'a') as logfile:
        logfile.write('{} - {}\n'.format(now(), msg))
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
