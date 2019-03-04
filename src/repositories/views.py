from django.shortcuts import render, redirect
from django.conf import settings
from .models import repositories
import os, sys, json, subprocess, re
from castic.globals import config, __shell__, __log__, loginRequired
from castic.settings import BASE_DIR

@loginRequired
def repos(request):
	'''
	fetch backup data from postgres and render it to template
	'''
	# get repo data and append snapshots-uri to link
	repos = list(repositories.objects.order_by('name').values())
	for repo in repos:
		repo['snapshotsURI'] = '/snapshots/{}'.format(repo['absolPath'].replace('/', '.'))

	general = {
		'hostname': __shell__('cat /etc/hostname').replace('\n',''),
		'path': config['general']['backupPath'],
		'space': __getFreeDiskSpace__(),
		'lastCheck': __getLastDate__(),
		'status': __getOverallHealth__()
	}
	return render(request, 'information.html', {'repos':repos, 'general':general})

def __getFreeDiskSpace__():
	'''
	This function returns str that describes available disk space and corresponding mount-path
	'''
	# get mount-point	
	root = os.path.join(config['general']['backupPath'], '')	# make sure path ends with /
	output = __shell__('df -h')

	mountPoint = __getMountPoint__(output, root) # fix this shit here: return value
	overallSpace, availableSpace = __getOverallSpace__(output, mountPoint)
	
	return '{} out of {} left on {}'.format(availableSpace, overallSpace, mountPoint)

def __getOverallSpace__(output, root):
	'''
	Return overall space of disk at mountpoint
	'''
	patternOverall = re.compile(r'\s+(\d+[A-Z]).+\s+(\d+[A-Z])\s+\d+%\s+{}[\n]'.format(root))
	patternAvailable = re.compile(r'(\d+[A-Z])\s+\d+%\s+{}[\n]'.format(root))
	return [(match.group(1), match.group(2)) for match in patternOverall.finditer(output)][0]

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
			return '/'

		# check if mountpoint exists
		for line in output.split('\n'):
			pattern = re.compile(r'({}/?)\n'.format(root))
			mountPoint = [ match.group(1) for match in pattern.finditer(line) ]
			if mountPoint:
				if len(mountPoint) != 1:
					return __log__('Fatal error in index/views __getFreeDiskSpace__(): len of matched disk-mounts != 1.')
				return mountPoint[0]


def __getLastDate__():
	'''
	This function returns last date of overall checks
	'''
	values = repositories.objects.values_list().values()

	# if empty, there was no initial check
	if not values:
		__shell__(os.path.join(BASE_DIR, 'bin/update.py'))
		return __getLastDate__()

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
