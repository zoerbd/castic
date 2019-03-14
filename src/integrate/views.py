from django.shortcuts import render, redirect
from django.conf import settings
from .forms import integrateInformation
import os, sys, json, subprocess, re, pdb, random, shutil
from subprocess import Popen, PIPE
from castic.globals import config, __shell__, loginRequired, gitProjectDir, __log__

# Create your views here.
@loginRequired
def integrate(request):
	'''
	Backend for ansible based automated integration
	'''
	if request.method == 'POST':
		form = integrateInformation(request.POST)
		if form.is_valid():
			rend = Rendering(form['user'].value(), form['password'].value(), 
					form['dest'].value(), form['repoPath'].value(), form['backupPath'].value(),
					form['localUser'].value(), form['localPassword'].value())
			rend.renderAnsible()
			result = rend.doIntegrationAndSavePW()
			return render(request, 'checkOutput.html', {'output':result})
		return redirect('/')
	config['general']['backupPath'] = os.path.join(config['general']['backupPath'], '')
	form = integrateInformation()
	return render(request, 'integrate.html', {"form":form, "config":config})

class Rendering:
	def __init__(self, user, pw, dest, repoPath, backupPath, localUser, localPassword, resticPW = ''.join([chr(random.randint(41,125)) for i in range(128)])):
		self.user = user
		self.pw = pw
		self.dest = dest
		self.repoPath = os.path.join(gitProjectDir, repoPath)
		self.backupPath = backupPath
		self.resticPW = resticPW
		self.localUser = localUser
		self.localPassword = localPassword
		self.ownHost = __shell__('cat /etc/hostname'.replace('\n', ''))

	def doIntegrationAndSavePW(self):
		'''
		This function executes the previously rendered ansible-backend
		and returns the exit message.
		'''
		result = __shell__('ansible-playbook ./integrate/ansible_rendered/setup.yml -e \"ansible_user={0}\" -e \"ansible_ssh_pass={1}\" -e \"ansible_become_pass={1}\"'.format(self.user, self.pw))
		passwdpath = os.path.join(gitProjectDir, 'passwords', ''.join(self.repoPath.split('/')[-1]))
		with open(passwdpath, 'w') as pwfile:
			pwfile.write(self.resticPW)
		if 'error' in result or 'Failed' in result or 'fatal' in result:
			__shell__('rm {}'.format(passwdpath))
			return __log__('Error occurred while trying to integrate: {}'.format(result))
		return result

	def renderAnsible(self):
			'''
			This function renders the ansible configuration and 
			roles and executes it after that on remote machine.
			Integration is based on shell script to integrate restic.
			'''
			originRoot = './integrate/ansible'
			renderedRoot = './integrate/ansible_rendered'

			# read recursively all ansible-files, return list with [<path>, <content>] for each file
			files = [ [os.path.join(root, filename), open(os.path.join(root, filename)).readlines()] 
			for root, subdirs, filenames in os.walk(originRoot) 
			for filename in filenames ]

			# parse and replace marked tags in ansible files
			pattern = re.compile(r'\?{2}(\w+)\?{2}')
			for pair in files:
				for line in pair[1]:
					updatedPair = [ [ pair[0].replace(originRoot, renderedRoot), 
									self.__doReplacement__(line, pattern) ]
									for line in pair[1] ]

				# recreate ansible files once (used decorator below)
				self.__createAnsibleFiles__(updatedPair)

				# write rendered content to new rendered files
				for filename, content in updatedPair:
					with open(filename, 'a') as fileobj:
						fileobj.write(''.join(content))
			shutil.copyfile(os.path.join(gitProjectDir, 'src/integrate/ansible_rendered/ansible.cfg'), '/etc/ansible/ansible.cfg')
			shutil.copyfile(os.path.join(gitProjectDir, 'src/integrate/ansible_rendered/hosts'), '/etc/ansible/hosts')
		
	def __doReplacement__(self, line, pattern):
		'''
		Called from __renderAnsible__.
		This function is used to avoid to compute same expression 
		two times in list comprehension, keep it more readable.
		-> Returns affected pattern and content to replace
		'''
		if line.count('?') < 4:
			return line
		for match in pattern.finditer(line):
			variable = match.group(1)
			line = line.replace('??{}??'.format(variable), eval('self.{}'.format(variable)).replace('\n', ''))
		return line

	def __createAnsibleFiles__(self, updatedPair):
		for filename, content in updatedPair:
			with open(filename, 'w') as fileobj:
				fileobj.write('')
