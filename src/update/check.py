from repositories.models import repositories
import os, sys, json, subprocess, re
from castic.globals import config, __shell__, __log__, gitProjectDir, __optionIsEnabled__
from castic.settings import BASE_DIR
from .mailing import mailingNotification
from repositories.views import __getFreeDiskSpace__
from django.utils.timezone import now

def checkRepositories():
	'''
	check if repos are healthty and update db-information
	'''
	appRoot = gitProjectDir      # used appRoot-var because it's better readable in my opinion

	# correct format of backupPath
	os.path.join(config['general']['backupPath'], '')

	# build path to repos based on given passwords
	repos = [ os.path.join(config['general']['backupPath'],directory)
			for directory in os.listdir(os.path.join(appRoot, 'passwords'))]

	# check if each corresponding repo is valid
	status = [ 'no error' in __shell__('restic -r {} --password-file {} --no-cache check'.format(
				repo, os.path.join(appRoot, 'passwords',
				repo.split('/')[-1]))) for repo in repos ]

	# update repository data in db
	for j,repo in enumerate(repos):
			statusNum = [1 if stat else 0 for stat in [status[j]]][0]
			repoSpace = __shell__('du -sh {}'.format(repo)).split('\t')[0]
			try:
					repositories.objects.update_or_create(
							name = repo.split('/')[-1],
							absolPath = repo,
							diskSpace = repoSpace,
							lastUpdate = now(), #--> doing that initially (defined in index/models.py)
							health = statusNum
					)
			except:
					col = repositories.objects.get(absolPath=repo)
					col.name = repo.split('/')[-1]
					col.diskSpace = repoSpace
					col.lastUpdate = now() #--> doing that initially (defined in index/models.py)
					col.health = statusNum
					col.save()

	# execute shell "command after"-option
	__shell__(config['check']['executeCommandAfterCheck'])

	# call diskSpace-warning if necessary
	__warnIfLowSpace__()

	# if enabled, send notification
	# -------------------------------
	result = ''

	if __optionIsEnabled__(config['notify']['sendMailNotifications']):
		result = mailingNotification().manageMailing()

	# if result returned something, an error occurred
	if result:
		__log__(result)
		return render(request, 'checkOutput.html', {'output':result})
	# -------------------------------

def __warnIfLowSpace__():
	'''
	Called from checkRepositories().
	Checks if disk space below notification-size.
	'''
	pattern = re.compile(r'(\d+[M|G|T])')
	space = list(pattern.finditer(__getFreeDiskSpace__()))[0].group(1)		# get available disk-space to plain '(\d+[M|G|T])'-str (default return shape= 'X out of Y left on .')
	minSpace = config['notify']['warnIfDiskSpaceSmallerThan']
	pattern = re.compile(r'\d+[M|G|T]')
	if not pattern.finditer(minSpace):
		return __log__('Invalid value for \'Warn if disk space smaller than\'-option.')
	
	# convert units if necessary
	# split into values- and units-part for easier processing
	values = [float(item[:-1]) for item in [space, minSpace]]
	units = [item[-1] for item in [space, minSpace]]

	# if unequal convert
	if units[0] != units[1]:
		order = ['M', 'G', 'T']
		exp = order.index(units[0]) - order.index(units[1])
		values[0] = values[0] * (1000 ** exp)
	
	# if available space below 'warnIfSpaceSmallerThan'-value, send warning log and mail if enabled
	if values[0] - values[1] < 0:
		return __log__('WARNING: Available disk space is below \'warnIfSpaceSmallerThan\'-value.\nMail-notification returned with: \'{}\'.'.format(mailingNotification().manageMailing()))

