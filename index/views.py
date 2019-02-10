from django.shortcuts import render, redirect
from django.conf import settings
from .models import repositories
import os, sys, json, subprocess, datetime, re

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
		'hostname': __shell__('cat /etc/hostname').replace('\n',''),
		'path': config['backupPath'],
		'space': __getFreeDiskSpace__(),
		'lastCheck': 'Nov. 12, 2018',
		'status': 'healthy'
	}
	return render(request, 'information.html', {'repos':repos, 'general':general})

def settings(request):
	conf = [ { 'value':list(config.values())[j], 'name':list(config.keys())[j]}
		for j in range(len(config)) ]
	return render(request, 'settings.html', {'config':conf})

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

def __getFreeDiskSpace__():
	'''
	This function returns available disk space and corresponding mount-path
	'''
	# get mount-point	
	root = config['backupPath'] + '/' # adding / very dirty waround
	output = __shell__('df -h')

	# iterate through possible mount-points by cutting /<something> after each iterat. 
	mountPoint = []	
	while not mountPoint:

		# update root by cutting last /<something>
		root = '/'.join(root.split('/')[:-1])

		# in last iteration root-var is enpty str, so mounted path is /
		if not root:
			root = '/'

		# check if mountpoint exists
		pattern = re.compile(r'({}/?)\n'.format(root))
		mountPoint = [match.group(1) for match in pattern.finditer(output)]

		if len(mountPoint) > 1:
			return __log__('Fatal err __getFreeDiskSpace__(): len of matched\
			disk-mounts > 1.')

	# get corresponding available space
	pattern = re.compile(r'(\d+\w)\s+\d%\s+{}\n'.format(root))
	availableSpace = [match.group(1) for match in pattern.finditer(output)]

	# get corresponding overall space
	pattern = pattern = re.compile(r'\s+(\d+\w+).+(\d+\w)\s+\d%\s+{}\n'.format(root))
	overallSpace = [match.group(1) for match in pattern.finditer(output)]
	
	return '{} out of {} left on {}'.format(availableSpace[0], overallSpace[0], mountPoint[0])

def __log__(msg):
	print(msg)
	return msg
