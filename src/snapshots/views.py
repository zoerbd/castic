from django.shortcuts import render, redirect
from castic.globals import loginRequired, __shell__, gitProjectDir
from .forms import restoreForm
from repositories.models import repositories
import re, os

@loginRequired
def snapshots(request, absolPath=None):
	'''
	backend for /snapshots/<repoPath>
	'''
	snaps = snapshotManagement(request).updateSnapshots(absolPath)
	form = restoreForm()
	if not snaps:
		snaps = '.'		# if error occurred, prevent from outputting empty template
	return render(request, 'snapshots.html', {'snaps':list(reversed(snaps)), 'form':form})

@loginRequired
def snapshot(request):
	'''
	Placeholder for root url of /snapshots/.
	'''
	return redirect('/')

@loginRequired
def delete(request, absolPath, snapID):
	'''
	backend for /snapshpots/<str:absolPath>/delete/<str:snapID>
	'''
	__shell__('restic -r {} forget {} --prune --password-file {}'.format(absolPath.replace('.', '/'), snapID, os.path.join(gitProjectDir, 'passwords', absolPath.split('.')[-1])))
	return redirect('/snapshots/{}'.format(absolPath))

@loginRequired
def restore(request, absolPath, snapID):
	'''
	backend for /snapshots/restore
	'''
	if request.method == 'POST':
		form = restoreForm(request.POST)
		if not form.is_valid():
			return render(request, 'checkOutput.html', {'output':'Form was not valid, sorry!'})
		__shell__('restic -r {} restore --no-cache {} --target {} --password-file {}'.format(absolPath.replace('.', '/'), snapID, form['restorePath'].value(), os.path.join(gitProjectDir, 'passwords', absolPath.split('.')[-1])))
	return redirect('/')

class snapshotManagement:
	def __init__(self, request, allRepos=None):
		self.allRepos = allRepos
		self.request = request

	def updateSnapshots(self, absolPath):
		'''
		This method is called from updateSnapshots 
		and returns correct formatted infro for each snapshot.
		'''
		absolPath = absolPath.replace('.', '/')
		passwordFile = os.path.join(gitProjectDir, 'passwords', absolPath.split('/')[-1])
		snapshots = __shell__('restic -r {} --password-file {} snapshots'.format(absolPath, passwordFile))
		return self.__formatSnapshotStr__(snapshots, absolPath)

	def __formatSnapshotStr__(self, snaps, absolPath):
		'''
		This method gets called from updateSnapshots 
		and returns snapshot list in format of:
		[
			{'absolPath': '<...>',
				'id':<...>,
				'created':<...>,
				'host':<...>,
				...
			},
			...
		]
		'''
		snapshots = []
		pattern = re.compile(r'(\w{8})\s+(\d{4}\-\d{2}\-\d{2}\s+\d{2}\:\d{2}\:\d{2})\s+([\w|\.|\-]+)\s+(/.*)')
		for match in pattern.finditer(snaps):
			snapshots.append({
				'absolPath' : absolPath,
				'pathURI' : absolPath.replace('/', '.'),
				'snapshotID' : match.group(1),
				'created': match.group(2),
				'host' : match.group(3),
				'paths' : match.group(4)
			})
		return snapshots

