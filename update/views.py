from django.shortcuts import render, redirect
from django.conf import settings
from .models import repositories
import os, sys, json, subprocess, datetime, re

# Create your views here.
def update(request):
        '''
        check if repos are healthty and update db
        '''
        appRoot = '/var/www/castic'#settings.BASE_DIR

        # correct format of backupPath
        if config['general']['backupPath'][-1] == '/':
                config['general']['backupPath'] = config['general']['backupPath'][:-1]

        # build path to repos based on given passwords
        repos = [ '{}/{}'.format(config['general']['backupPath'], directory)
                for directory in os.listdir(appRoot + '/passwords')]

        # check if each corresponding repo is valid
        status = [ 'no error' in __shell__('restic -r {} --password-file {} \
                --no-cache check'.format(repo, appRoot + '/passwords/'
                + repo.split('/')[-1])) for repo in repos ]

        # update repository data in db
        for j,repo in enumerate(repos):
                statusNum = [1 if stat else 0 for stat in [status[j]]][0]
                repoSpace = __shell__('du -sh {}'.format(repo)).split('\t')[0]
                try:
                        repositories.objects.update_or_create(
                                name = repo.split('/')[-1],
                                absolPath = repo,
                                diskSpace = repoSpace,
                                lastUpdate = datetime.datetime.now(),
                                health = statusNum
                        )
                except:
                        col = repositories.objects.get(absolPath=repo)
                        col.name = repo.split('/')[-1]
                        col.diskSpace = repoSpace
                        col.lastUpdate = datetime.datetime.now()
                        col.health = statusNum
                        col.save()
        return redirect('/')

def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        return subprocess.check_output(command, shell=True).decode('utf-8')
