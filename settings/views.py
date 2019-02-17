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
                {'category':cat, 'content':[
                        [{'key':key, 'value':config[cat][key]} for key in list(config[cat].keys())]
                ][0]} 
                for cat in categories
        ]
        #return render(request, 'checkOutput.html', {'output':cats[1]['content'][2]['key']})#['content'][0]['key']})

        if request.method == 'POST':
                form = settingsForm(request.POST)
                if form.is_valid():
                        newConf = __updateConfig__(form.cleaned_data)
                        return render(request, 'checkOutput.html', {"output" : newConf})
                return render(request, 'checkOutput.html', {"output" : 'Form was invalid!'})

        # prepare initial values from config file
        initialValues = [
                [{value['key']:value['value']}
                for value in cat['content']]
                for cat in cats
        ]
        new = initialValues[0][0]
        for category in initialValues:
                for j in range(1, len(category)):
                        print(category[j])
                        new.update(**category[j-1], **category[j])
        #initialValues = {**initialValues[0], **initialValues[1], **initialValues[2]}    # merge initial values - fix this later to be more dynamic

        form = settingsForm(initial=initialValues)
        return render(request, 'settings.html', {"categories":categories, "cats":cats, "form":form})

def __updateConfig__(conf):
        return json.dumps(conf, ensure_ascii=False)                