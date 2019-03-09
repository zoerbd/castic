from django.shortcuts import render, redirect
from .forms import settingsForm
import json, shutil, re, os
from castic.globals import config, loginRequired, __log__, gitProjectDir
from castic.settings import BASE_DIR
from repositories.models import repositories

# Create your views here.
@loginRequired
def settings(request):
        '''
        Backend for settings-page.
        Created dynamically, based on config.json.
        '''
        categories = list(config.keys())
        cats = [
                {'category':cat, 'content':[
                        [{'key':key, 'value':config[cat][key]} for key in list(config[cat].keys())]
                ][0]} 
                for cat in categories
        ]

        if request.method == 'POST':
                form = settingsForm(request.POST)
                if form.is_valid():
                        newConf = __updateConfig__(config, form.cleaned_data)

                        # write out new config
                        configPath = os.path.join(gitProjectDir, 'config.json')
                        shutil.copyfile(configPath, configPath + '.orig')
                        with open(configPath, 'w') as wfile:
                                wfile.write(newConf)

                        __log__(checkAndForgetAutomation(newConf).updateAll())
                        return redirect('/settings/')
                return render(request, 'checkOutput.html', {"output" : __log__('Form was invalid!')})

        # prepare initial values from config file
        initialValues = [
                [{value['key']:value['value']}
                for value in cat['content']]
                for cat in cats
        ]

        # merge initial values - fix this later to be more dynamic and less spaghetti
        newInitialValues = initialValues[0][0]
        for categ in initialValues:
                for j in range(1, len(categ)):
                        newInitialValues.update(**categ[j-1], **categ[j])

        form = settingsForm(initial=newInitialValues)
        return render(request, 'settings.html', {"categories":categories, "cats":cats, "form":form})

def __updateConfig__(confOrig, confNew):
        '''
        This function is called from settings().
        It returns the updated config as JSON string
        (Basically also solves the problem that the backend 
        returns a non categorized settings-dict
        '''
        for section in confOrig:
                for key in confNew:
                        try:
                                confOrig[section][key]
                                confOrig[section][key] = confNew[key]
                        except:
                                pass
        return json.dumps(confOrig, ensure_ascii=False)


class checkAndForgetAutomation:
        def __init__(self, conf):
                self.conf = conf

        def updateAll(self):
                '''
                This function is called from settings() out of settings/views.
                It updates users cronjob for doing AutoCheck.
                '''

                values = {
                        'check' : {
                                'col' : [
                                        'check',
                                        'autoCheck'
                                ],
                                'interval' : '24h',      # default value
                                'method' : 'self.__generateCheckCronjobStr__()',
                                'task_pattern' : '/bin/update.py',
                                'pattern' : r'[False|\d+[h|m]]'
                        },
                        'forget' : {
                                'col': [
                                        'general',
                                        'autoForgetAll'
                                ],
                                'interval' : '8',         # default value
                                'method' : 'self.__generateForgetCronjobStr__()',
                                'task_pattern': 'forget --prune --keep-last',
                                'pattern' : r'[False|\d+]'

                        }
                }

                for automationMethod in values.keys():
                        methodname = values[automationMethod]
                        self.pattern = methodname['pattern']    # pattern for syntax check
                        self.task_pattern = methodname['task_pattern']

                        self.interval = json.loads(self.conf)[methodname['col'][0]][methodname['col'][1]]
                        if self.__checkAutoCheckSyntax__():
                                self.interval = methodname['interval']
                        cronjob = eval(methodname['method'])

                        # replace in crontab-file if actual cronjobStr in cronjob-var (instead of error -> either result or error is returned)
                        if '* * *' in cronjob:
                                __log__(self.__replaceOrCreateCronjob__(cronjob))
                        else:
                                __log__('Error occurred while trying to create cronjobs in settings/views.py.\nOutput: {}'.format(cronjob))

        def __replaceOrCreateCronjob__(self, cronjobStr):
                '''
                This function is called from __updateAutoCheck__() out of settings/views. 
                It replaces the cronjob for automating the backup check.
                Returns error-str if an exception occurrs. 
                '''
                crontabPath = '/var/spool/cron/crontabs/root'    # maybe make this as setting available later
                if not os.path.isdir(crontabPath.replace('root', '')):
                        newCrontabPath = crontabPath.split('/')
                        newCrontabPath.remove(newCrontabPath[-2])
                        crontabPath = '/'.join(newCrontabPath)
                try:
                        shutil.copyfile(crontabPath, crontabPath + '.orig')     # save backup file in case of bugs/exceptions
                except FileNotFoundError:
                        with open(crontabPath, 'w') as cronfile:
                                cronfile.write('# created by castic\n')
                        return self.__replaceOrCreateCronjob__(cronjobStr)
                with open(crontabPath, 'r') as crontab:
                        crontabContent = crontab.readlines()
                
                # replace current cronjob, if none set, append
                for j, line in enumerate(crontabContent):
                        if  self.task_pattern  in line:
                                crontabContent[j] = ''
                crontabContent.append(cronjobStr)

                # write out new cronjob
                with open(crontabPath, 'w') as crontab:
                        crontab.write(''.join(crontabContent))

        def __checkAutoCheckSyntax__(self):
                '''
                This function is called from __updateAutoCheck__() out of settings/views.
                Returns error-str if input is invalid.
                '''
                pattern = re.compile(self.pattern)
                if not pattern.finditer(self.interval):
                        return __log__('Got invalid syntax in AutoCheck/AutoForget setting.\nGiven value {}.'.format(self.interval))

        def __generateCheckCronjobStr__(self):
                '''
                This function is called from __updateAutoCheck__() out of settings/views. 
                It generates the cronjob for automating the backup check.
                Returns error-str if an exception occurrs.
                '''
                if not self.interval:
                        return __log__('AutoCheck disabled in settings.')
                cronjob = 'm h * * *  {}\n'.format(os.path.join(BASE_DIR, 'bin/update.py'))

                # get number of interval in int
                checkIntervalNumber = int(self.interval.replace('h', '').replace('m', ''))      

                if 'h' in self.interval:
                        return cronjob.replace('m h', '0 */{}'.format(int(checkIntervalNumber)))
                return cronjob.replace('m h', '*/{} 0'.format(int(checkIntervalNumber)))

        def __generateForgetCronjobStr__(self):
                '''
                This function is called from __updateAutoCheck__() out of settings/views. 
                It generates the cronjob for automating the backup forget.
                Returns error-str if an exception occurrs.
                '''
                if not self.interval:
                        return __log__('AutoForget disabled in settings.')

                return ''.join([ '{} * * *  {}\n'.format(self.__getCronTime__(j), 'restic -r {}\
                        --password-file {} forget --prune --keep-last {}'.format(repo.absolPath, os.path.join(gitProjectDir, 'passwords',  repo.absolPath.split('/')[-1]), self.interval))
                        for j, repo in enumerate(repositories.objects.all()) ])

        def __getCronTime__(self, index):
                '''
                This function is called from __generateForgetCronjobStr__() out of settings/views. 
                Returns first two nums of cronjob.
                '''
                index *= 20
                return '{} {}'.format(int(index%60), int(index/60))