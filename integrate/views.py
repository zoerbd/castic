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
			files = Rendering(form['user'].value(), form['password'].value(), 
			form['dest'].value(), form['repoPath'].value(), form['backupPath'].value()).renderAnsible()
			return render(request, 'checkOutput.html', {'output':files})
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

	def renderAnsible(self):
			'''
			This function renders the ansible configuration and 
			roles and executes it on after that on remote machine.
			Integration is based on my shell script to integrate restic.
			'''
			originRoot = './integrate/ansible'
			renderedRoot = './integrate/.ansible_rendered'

			# read recursively all ansible-files, return list with [<path>, <content>] for each file
			files = [ [os.path.join(root, filename), open(os.path.join(root, filename)).readlines()] 
			for root, subdirs, filenames in os.walk(originRoot) 
			for filename in filenames ]

			# save rendered stuff to new dir later on
			try:
				os.mkdir(renderedRoot)
			except:
				pass

			# parse and replace marked tags in ansible files
			pattern = re.compile(r'.*\?{2}(\w+)\?{2}')
			for pair in files:
				#updatedPair = [ [path.replace(originRoot, renderedRoot), __doReplacement__(line, pattern.finditer(line).group(1).strip()) ]
					#for path, content in pair 
					#for line in content ]
				for line in pair[1]:
					a = [[pair[0].replace(originRoot, renderedRoot), self.__doReplacement__(line, match.group(1).strip())]
						for match in pattern.finditer(line)]

				# write rendered content to new rendered files
				#[ open(filename, 'w').write(''.join(content)) 
				#	for filename, content in updatetPair ]
			return 

	def __doReplacement__(self, line, variable):
		'''
		Called from __renderAnsible__.
		This function is used  for avoiding to compute same 
		expression two times in list comprehension and keep it more readable.
		-> Returns affected pattern and content to replace
		'''
		if not variable in line:
			return line
		return line.replace('??{}??'.format(variable), eval('self.{}'.format(variable)))
