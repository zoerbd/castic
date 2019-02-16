from django.shortcuts import render, redirect
from django.conf import settings
from .forms import integrateInformation
import os, sys, json, subprocess, re, pdb

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
			render = Rendering(form['user'].value(), form['password'].value(), 
					form['dest'].value(), form['repoPath'].value(), form['backupPath'].value())
			render.renderAnsible()
			result = render.doIntegration()
			return render(request, 'checkOutput.html', {'output':result})
		return redirect('/')
	if config['general']['backupPath'][-1] != '/':
		config['general']['backupPath'] += '/'
	form = integrateInformation() #initial={'repoPath': 'autofillComingSoon!'})
	return render(request, 'integrate.html', {"form":form, "config":config})


def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        return subprocess.check_output(command, shell=True).decode('utf-8')

class Rendering:
	def __init__(self, user, pw, dest, repoPath, backupPath, resticPW = None):
		self.user = user
		self.pw = pw
		self.dest = dest
		self.repoPath = repoPath
		self.backupPath = backupPath
		self.resticPW = resticPW

	def doIntegration(self):
		'''
		This function executes the previously rendered ansible-backend
		and returns the exit message.
		'''
		return __shell__('ansible-playbook ./ansible_rendered/setup.yml -e \"ansible_user={0} ansible_ssh_pass={1} ansible_sudo_pass={1}\"'.format(self.user, self.pw))

	def renderAnsible(self):
			'''
			This function renders the ansible configuration and 
			roles and executes it on after that on remote machine.
			Integration is based on my shell script to integrate restic.
			'''
			originRoot = './integrate/ansible'
			renderedRoot = './integrate/ansible_rendered'

			# read recursively all ansible-files, return list with [<path>, <content>] for each file
			files = [ [os.path.join(root, filename), open(os.path.join(root, filename)).readlines()] 
			for root, subdirs, filenames in os.walk(originRoot) 
			for filename in filenames ]

			# parse and replace marked tags in ansible files
			pattern = re.compile(r'.*\?{2}(\w+)\?{2}')
			peter = []
			for pair in files:
				for line in pair[1]:
					updatedPair = [ [ pair[0].replace(originRoot, renderedRoot), 
									self.__doReplacement__(line, match.group(1).strip()) ]
									for match in pattern.finditer(line) ]
					try:
						os.system('mkdir -p {}'.format(''.join(updatedPair[0][0].split('/')[:-1])))
					except:
						pass
					peter.append(updatedPair)
				# write rendered content to new rendered files
				#[ open(filename, 'w').write(''.join(content)) 
				#	for filename, content in updatedPair ]
				for filename, content in updatedPair:
					fileobj = open(filename, 'w')
					fileobj.write(''.join(content))
					fileobj.close()
			return files

	def __doReplacement__(self, line, variable):
		'''
		Called from __renderAnsible__.
		This function is used  for avoiding to compute same 
		expression two times in list comprehension and keep it more readable.
		-> Returns affected pattern and content to replace
		'''
		if line.count('?') < 4:
			return line
		return line.replace('??{}??'.format(variable), eval('self.{}'.format(variable)))
