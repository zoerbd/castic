from django.shortcuts import render, redirect
from django.conf import settings
from .models import repositories
import os, sys, json, subprocess, datetime

# read config file
with open('config.json') as jsonFile:
	config = json.load(jsonFile)

# Create your views here.
def index(request):
	'''
	fetch backup data from postgres and render it to template
	'''
	repos = repositories.objects.values_list().values()
	general = {
		'hostname': 'host.tld',
		'path': config['backupPath'],
		'space': '2.5TB',
		'lastCheck': 'Nov. 12, 2018',
		'status': 'healthy'
	}
	return render(request, 'information.html', {'repos':repos, 'general':general})

def settings(request):
	return render(request, 'settings.html')

def docs(request):
	return render(request, 'docs.html')

def update(request):
	'''
	check if repos are healthty and update db
	'''
	appRoot = '/var/www/castic'#settings.BASE_DIR

	# correct format of backupPath
	if config['backupPath'][-1] == '/':
		config['backupPath'] = config['backupPath'][:-1]
	
	# build path to repos based on given passwords
	repos = [ '{}/{}'.format(config['backupPath'], directory) 
		for directory in os.listdir(appRoot + '/passwords')]

	# check if each corresponding repo is valid
	status = [ 'no error' in __shell__('restic -r {} --password-file {} \
		--no-cache check'.format(repo, appRoot + '/passwords/'
		+ repo.split('/')[-1])) for repo in repos ]

	# update repository data in db
	for j,repo in enumerate(repos):
		statusNum = [1 if stat else 0 for stat in [status[j]]][0]
		repositories.objects.update_or_create(
			name = repo.split('/')[-1],
			absolPath = repo,
			diskSpace = '1.2TB', #__shell__('du -sh {}'.format(repo)).split(' ')[0],
			lastUpdate = datetime.datetime.now(),
			health = statusNum
		)
	return redirect('/')

def __shell__(command):
	'''
	This function makes it less pain to get shell answers
	'''
	return subprocess.check_output(command, shell=True).decode('utf-8')
