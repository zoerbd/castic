from index.models import repositories
import os, sys, json, subprocess, datetime, re
from webmanagement.settings import config, BASE_DI


        '''
        check if repos are healthty and update db
        '''
        appRoot = BASE_DIR      # used appRoot-var because it's better readable in my opinion

        # correct format of backupPath
        os.path.join(config['general']['backupPath'], '')

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

        # execute shell "command after"-option
        os.system(config['check']['executeCommandAfterCheck'])