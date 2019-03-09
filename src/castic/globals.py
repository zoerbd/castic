# ------------------------------------------------------------>
# ---- Globally used config-vars and function defined here ---

import json, subprocess, os, sys, re
sys.path.insert(0, '/var/www/castic/src')
from django.shortcuts import redirect
from django.utils.timezone import now
from castic.settings import BASE_DIR

# read config file
gitProjectDir = '/'.join(BASE_DIR.split('/')[:-1])   # get parent dir of src
with open(os.path.join(gitProjectDir, 'config.json')) as jsonFile:
        config = json.load(jsonFile)

def __shell__(command, old=False):
        '''
        This function makes it less pain to get shell answers
        '''
        if old:
            return subprocess.check_output(command, shell=True).decode('utf-8').strip()
        process = subprocess.Popen(command.split(' '), stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, stderr = [ item.decode('utf-8').strip() for item in process.communicate()]
        if stderr:

            # avoiding unlocked repository errors by unlocking and cleaning cache
            if 'restic -r' in command and 'locked' in stderr:
                err = ''        # prevent from beeing undefined in return __log__
                pattern = re.compile(r'restic\s\-r\s(.+)\s.*\-\-password\-file\s(.+)[\s|\n]')

                # may fail because of possible wrong command formatting -> group(1) or group(2) not existing
                try:
                    for match in pattern.finditer(command):
                        repo = match.group(1)
                        pwFile = match.group(2)
                    __shell__('restic -r {} --no-cache --cleanup-cache unlock --password-file {}'.format(repo, pwFile))
                    return __shell__(command)
                except Exception as err:
                    err = '\nTried to unlock repo but another exception occurred: {}.'.format(err)

                return __log__("Shell command failed with: {}.{}".format(stderr, err))
        return stdout
       
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
