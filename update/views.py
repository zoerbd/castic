from django.shortcuts import render, redirect
from django.conf import settings
from index.models import repositories
import os, sys, json, subprocess, datetime, re, threading
from castic.globals import config, __shell__, loginRequired, __log__
from castic.settings import BASE_DIR
from .check import checkRepositories
from .mailing import mailingNotification

# Create your views here.
@loginRequired
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
                __log__(result)
                return render(request, 'checkOutput.html', {'output':result})
        return redirect('/')

