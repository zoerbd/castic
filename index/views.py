from django.shortcuts import render, redirect
from django.conf import settings
from .models import repositories
import os, sys, json, subprocess, datetime, re

# read config file
with open('config.json') as jsonFile:
	config = json.load(jsonFile)

def index(request):
	'''
	check if user is authenticated and 
	fetch backup data from postgres and render it to template
	'''
	if request.root.is_authenticated:
		repos = repositories.objects.values_list().values()
		general = {
			'hostname': __shell__('cat /etc/hostname').replace('\n',''),
			'path': config['general']['backupPath'],
			'space': __getFreeDiskSpace__(),
			'lastCheck': __getLastDate__(),
			'status': __getOverallHealth__()
		}
		return render(request, 'information.html', {'repos':repos, 'general':general})
	return redirect('/login')

def settings(request):
	'''
	Backend for settings-page.
	Created dynamically, based on config.json.
	'''
	cats = list(config.keys())
	catsContent = [[{'key':list(config[cat].keys())[i], 'value':
			list(config[cat].values())[i]} for i in 
			range(len(list(config[cat].keys())))] for cat in cats]

	return render(request, 'settings.html', {"cats":cats, 
	"content":catsContent})

def docs(request):
	return render(request, 'docs.html')

def update(request):
	'''
	check if repos are healthty and update db
	'''
	appRoot = '/var/www/castic'#settings.BASE_DIR

	# correct format of backupPath
	if config['general']['backupPath'][-1] == '/':
		config['general']['backupPath'] = config['general']['backupPath'][:-1]
	
	# build path to repos based on given passwords
	repos = [ '{}/{}'.format(config['general']['backupPath'], directory) 
		for directory in os.listdir(appRoot + '/passwords')]

	# check if each corresponding repo is valid
	status = [ 'no error' in __shell__('restic -r {} --password-file {} \
		--no-cache check'.format(repo, appRoot + '/passwords/'
		+ repo.split('/')[-1])) for repo in repos ]

	# update repository data in db
	for j,repo in enumerate(repos):
		statusNum = [1 if stat else 0 for stat in [status[j]]][0]
		repoSpace = __shell__('du -sh {}'.format(repo)).split('\t')[0]
		try:
			repositories.objects.update_or_create(
				name = repo.split('/')[-1],
				absolPath = repo,
				diskSpace = repoSpace,
				lastUpdate = datetime.datetime.now(),
				health = statusNum
			)
		except:
			col = repositories.objects.get(absolPath=repo)
			col.name = repo.split('/')[-1]
			col.diskSpace = repoSpace
			col.lastUpdate = datetime.datetime.now()
			col.health = statusNum
			col.save()
	return redirect('/')

def __shell__(command):
	'''
	This function makes it less pain to get shell answers
	'''
	return subprocess.check_output(command, shell=True).decode('utf-8')

def __getFreeDiskSpace__():
	'''
	This function returns str that describes available disk space and corresponding mount-path
	'''
	# get mount-point	
	root = config['general']['backupPath'] + '/' # adding /: very dirty waround
	output = __shell__('df -h')

	mountPoint = __getMountPoint__(output, root) # fix this shit here: return value
	availableSpace = __getAvailableSpace__(output, mountPoint)
	overallSpace = __getOverallSpace__(output, mountPoint)
	
	return '{} out of {} left on {}'.format(availableSpace, overallSpace, mountPoint)

def __getOverallSpace__(output, root):
	'''
	Return overall space of disk at mountpoint
	'''
	pattern = re.compile(r'\s+(\d+\w+).+(\d+\w)\s+\d%\s+{}\n'.format(root))
	return [match.group(1) for match in pattern.finditer(output)][0]

def __getMountPoint__(output, root):
	'''
	Return mountpoint of backup-disk
	'''
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
			return __log__('Fatal err __getFreeDiskSpace__(): len of matched disk-mounts > 1.')
	return mountPoint[0]

def __getAvailableSpace__(output, root):
	'''
	Return available disk-space of mount-points disk
	'''
	pattern = re.compile(r'(\d+\w)\s+\d%\s+{}\n'.format(root))
	return [match.group(1) for match in pattern.finditer(output)][0]

def __log__(msg):
	print(msg)
	return msg

def __getLastDate__():
	'''
	This function returns last date of overall checks
	'''
	values = repositories.objects.values_list().values()
	for j in range(1, len(values)):
		latest = values[j]['lastUpdate']
		if values[j-1]['lastUpdate'] > latest:
			latest = values[j-1]['lastUpdate']
	return latest

def __getOverallHealth__():
	'''
	This function returns last state of overall health.
	If any repository is unhealthy -> overall unhealthy,
	Else healthy.
	'''
	values = repositories.objects.values_list().values()
	for value in values:
		if not value['health']:
			return 0
	return 1
