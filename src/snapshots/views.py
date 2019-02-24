from django.shortcuts import render, redirect
from castic.globals import loginRequired, __shell__, gitProjectDir
from .models import snapshots
from repositories.models import repositories
import re, os

# Create your views here.
@loginRequired
def repos(request):
	'''
	backend for /snapshots/
	'''
	repos = [{'name': entry['absolPath'], 'nameURL': entry['absolPath'].replace('/', '.')} for entry in list(repositories.objects.values())]
	return render(request, 'snapshots_index.html', {'repos': repos})

@loginRequired
def snapshots(request, absolPath=None):
	'''
	backend for /snapshots/<repoPath>
	'''
	snaps = snapshotManagement(request).updateSnapshots(absolPath)
	return render(request, 'snapshots.html', {'snaps':snaps})

class snapshotManagement:
	def __init__(self, request, allRepos=None):
		self.allRepos = allRepos
		self.request = request

	def updateSnapshots(self, repo=None):
		'''
		This method is mainly called from from snapshots 
		and updates all snapshot data for one or all repos.
		'''
		if repo:
			repo = repo.replace('.', '/')
			return self.__getSnapshotsInfo__(repo)

		snapshots = []
		for repo in self.allRepos:
			snapshots.append(self.__renderSnapshotsForRepo__(repo, __getSnapshotsInfo__(repo)))
		return self.__insertIntoDB__(snapshots)

	def __insertIntoDB__(self, snapshots):
		'''
		This method gets called from updateSnapshots in case of snapshot-information caching.
		It writes the previously generated snapshots from variable to the prepared model.
		Structure of snapshots-variable:
		[
			{'absolPath':<...>, ...allOtherAttributes....},
			{'absolPath':<...>, ...allOtherAttributes....},
							.
							.
			{'absolPath':<...>, ...allOtherAttributes....}
		]
		'''
		return True

	def __getSnapshotsInfo__(self, absolPath):
		'''
		This method is called from updateSnapshots 
		and returns correct formatted infro for each snapshot.
		'''
		passwordFile = os.path.join(gitProjectDir, 'passwords', absolPath.split('/')[-1])
		snapshots = __shell__('restic -r {} --password-file {} snapshots'.format(absolPath, passwordFile))
		return self.__formatSnapshotStr__(snapshots, absolPath)

	def __formatSnapshotStr__(self, snaps, absolPath):
		'''
		This method gets called from __getSnapshotsInfo__ 
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
		pattern = re.compile(r'(\w{8})\s+(\d{4}\-\d{2}\-\d{2}\s+\d{2}\:\d{2}\:\d{2})\s+(\w+\.\w+)\s+(/.+)')
		for match in pattern.finditer(snaps):
			snapshots.append({
				'absolPath' : absolPath,
				'snapshotID' : match.group(1),
				'created': match.group(2),
				'host' : match.group(3),
				'paths' : match.group(4)
			})
		return snapshots

