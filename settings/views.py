from django.shortcuts import render
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
        cats = list(config.keys())
        catsContent = [[{'key':list(config[cat].keys())[i], 'value':
                        list(config[cat].values())[i]} for i in
                        range(len(list(config[cat].keys())))] for cat in cats]

        return render(request, 'settings.html', {"cats":cats, "content":catsContent})
