from django.shortcuts import render, redirect
from .forms import settingsForm
import json, shutil
from webmanagement.settings import config

# Create your views here.
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
                        shutil.copyfile('config.json', 'config.json.orig')
                        with open('config.json', 'w') as wfile:
                                wfile.write(newConf)

                        return redirect('/settings/')
                return render(request, 'checkOutput.html', {"output" : 'Form was invalid!'})

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