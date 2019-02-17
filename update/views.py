from django.shortcuts import render, redirect
from django.conf import settings
from index.models import repositories
import os, sys, json, subprocess, datetime, re, threading
from webmanagement.settings import config, BASE_DIR, __shell__
from .check import checkRepositories
from .mailing import mailingNotification

# Create your views here.
def update(request):
        if eval(config['check']['DoCheckInBackground']):
                threading.Thread(target=checkRepositories).start()
        else:
                checkRepositories() 

        # if enabled, send notification
        #result = mailingNotification().manageMailing()
        result = ''

        # if result returned something, an error occurred
        if result:
                return render(request, 'checkOutput.html', {'output':result})
        return redirect('/')

