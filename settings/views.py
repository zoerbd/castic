from django.shortcuts import render
from .forms import settingsForm
import json

# read config file
with open('config.json') as jsonFile:
        config = json.load(jsonFile)

# Create your views here.
def settings(request):
        '''
        Backend for settings-page.
        Created dynamically, based on config.json.
        '''
        categories = list(config.keys())
        cats = [
                [ {'category':cat, 'content':[
                        {'key':key, 'value':config[cat][key]}
                ]} 
                for key in list(config[cat].keys()) ][0]
                for cat in categories
        ]

        if request.method == 'POST':
                form = settingsForm(request.POST)
                if form.is_valid():
                        newConf = __updateConfig__(form.cleaned_data)
                        return render(request, 'checkOutput.html', {"output" : newConf})
                return render(request, 'checkOutput.html', {"output" : 'Form was invalid!'})
        form = settingsForm()
        return render(request, 'settings.html', {"cats":categories, "content":cats, "form":form})

def __updateConfig__(conf):
        return json.dumps(conf, ensure_ascii=False)                