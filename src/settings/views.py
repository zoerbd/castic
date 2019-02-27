from django.shortcuts import render, redirect
from .forms import settingsForm
import json, shutil, re, os
from castic.globals import config, loginRequired, __log__, gitProjectDir
from castic.settings import BASE_DIR

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

                        __log__(__updateAutoCheck__(newConf))
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

def __updateAutoCheck__(conf):
        '''
        This function is called from settings() out of settings/views.
        It updates users cronjob for doing AutoCheck (simply call /update on given time).
        '''
        checkInterval = json.loads(conf)['check']['autoCheck']
        if __checkAutoCheckSyntax__(checkInterval):
                checkInterval = '24h'
        cronjob = __generateCronjobStr__(checkInterval)

        # replace in crontab-file if actual cronjobStr in cronjob-var (instead of error)
        if '* * *' in cronjob:
                return __log__(__replaceAutoCheckCronjob__(checkInterval, cronjob))

def __checkAutoCheckSyntax__(checkInterval):
        '''
        This function is called from __updateAutoCheck__() out of settings/views.
        Returns error-str if input is invalid.
        '''
        pattern = re.compile(r'[False|\d+[h|m]]')
        if not pattern.finditer(checkInterval):
                return __log__('Got invalid syntax in AutoCheck setting.\nRestoring to default value of 24h\nGiven value {}.'.format(checkInterval))

def __generateCronjobStr__(checkInterval):
        '''
        This function is called from __updateAutoCheck__() out of settings/views. 
        It generates the cronjob for automating the backup check.
        Returns error-str if an exception occurrs.
        '''
        if not checkInterval:
                return __log__('AutoCheck disabled in settings.')
        cronjob = 'm h * * *  {}'.format(os.path.join(BASE_DIR, 'bin/update.py'))

        # get number of checkInterval in int
        checkIntervalNumber = int(checkInterval.replace('h', '').replace('m', ''))      

        if 'h' in checkInterval:
                return cronjob.replace('m h', '0 */{}'.format(int(checkIntervalNumber)))
        return cronjob.replace('m h', '*/{} 0'.format(int(checkIntervalNumber)))

def __replaceAutoCheckCronjob__(checkInterval, cronjobStr):
        '''
        This function is called from __updateAutoCheck__() out of settings/views. 
        It replaces the cronjob for automating the backup check.
        Returns error-str if an exception occurrs. 
        '''
        crontabPath = '/var/spool/cron/root'    # maybe make this as setting available later
        shutil.copyfile(crontabPath, crontabPath + '.orig')     # save backup file in case of bugs/exceptions
        with open(crontabPath, 'r') as crontab:
                crontabContent = crontab.readlines()
        
        # replace current cronjob, if none set, append
        for j, line in enumerate(crontabContent):
                if os.path.join(BASE_DIR, 'bin/update.py') in line:
                        crontabContent[j] = cronjobStr
                elif j == len(crontabContent) - 1:
                        crontabContent.append(cronjobStr)

        # write out new cronjob
        with open(crontabPath, 'w') as crontab:
                crontab.write(''.join(crontabContent))