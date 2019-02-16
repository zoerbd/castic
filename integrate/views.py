from django.shortcuts import render, redirect
from django.conf import settings
from .forms import integrateInformation
import os, sys, json, subprocess

# read config file
with open('config.json') as jsonFile:
	config = json.load(jsonFile)

# Create your views here.
def integrate(request):
	'''
	Backend for ansible based automated integration
	'''
	if request.method == 'POST':
		form = integrateInformation(request.POST)
		if form.is_valid():
			__renderAnsible__(form['user'].value(), form['password'].value(), 
			form['dest'].value(), form['resticPassword'].value(), form['repoPath'].value())
		return redirect('/')
	if config['general']['backupPath'][-1] != '/':
		config['general']['backupPath'] += '/'
	form = integrateInformation(initial={'repoPath': 'autofill from dest coming soon!'})
	return render(request, 'integrate.html', {"form":form, "config":config})


def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        return subprocess.check_output(command, shell=True).decode('utf-8')

def __renderAnsible__(user, pw, dest, resticPW, repoPath):
		'''
		This function renders the ansible configuration and 
		roles and executes it on after that on remote machine.
		Integration is based on my shell script to integrate restic.
		'''
		# read recursively all ansible-files, return list with [<path>, <content>] for each file
		files = [ [os.path.join(root, filename), os.path.join(root, filename).readlines()] 
		for root, subdirs, filenames in os.walk('./integrate/ansible') 
		for filename in filenames ]

