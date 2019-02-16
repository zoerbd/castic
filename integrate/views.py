from django.shortcuts import render, redirect
from django.conf import settings
from .forms import integrateInformation
import os, sys, json, subprocess, re, pdb, random
from subprocess import Popen, PIPE

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
			rend = Rendering(form['user'].value(), form['password'].value(), 
					form['dest'].value(), form['repoPath'].value(), form['backupPath'].value())
			rend.renderAnsible()
			result = rend.doIntegrationAndSavePW()
			return render(request, 'checkOutput.html', {'output':result})
		return redirect('/')
	config['general']['backupPath'] = os.path.join(config['general']['backupPath'], '')
	form = integrateInformation()
	return render(request, 'integrate.html', {"form":form, "config":config})


def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        return subprocess.check_output('{} 2>&1'.format(command), shell=True).decode('utf-8')

class Rendering:
	def __init__(self, user, pw, dest, repoPath, backupPath, resticPW = ''.join([chr(random.randint(41,125)) for i in range(128)])):
		self.user = user
		self.pw = pw
		self.dest = dest
		self.repoPath = repoPath
		self.backupPath = backupPath
		self.resticPW = resticPW
		self.ownHost = __shell__('cat /etc/hostname'.replace('\n', ''))

	def doIntegrationAndSavePW(self):
		'''
		This function executes the previously rendered ansible-backend
		and returns the exit message.
		'''
		result = Popen( [ 'ansible-playbook', './integrate/ansible_rendered/setup.yml', '-e', 
						'\"ansible_user={0} ansible_ssh_pass={1} ansible_sudo_pass={1}\"'.format(self.user, self.pw) ], 
						stdout = PIPE, stderr = PIPE)
		with open(os.path.join('./passwords', self.dest), 'w') as pwfile:
			pwfile.write(self.resticPW)
		return ''.join([line.decode('utf-8') for line in result.communicate()])

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
									self.__doReplacement__(line, match.group(1)) ]
									for match in pattern.finditer(line) ]
					try:
						os.system('mkdir -p {}'.format(''.join(updatedPair[0][0].split('/')[:-1])))
					except:
						pass
					peter.append(updatedPair)
				# write rendered content to new rendered files
				for filename, content in updatedPair:
					with open(filename, 'w') as fileobj:
						fileobj.write(''.join(content))
			print(peter)
			return 0

	def __doReplacement__(self, line, variable):
		'''
		Called from __renderAnsible__.
		This function is used to avoid to compute same expression 
		two times in list comprehension, keep it more readable.
		-> Returns affected pattern and content to replace
		'''
		pdb.set_trace()
		if line.count('?') < 4:
			return line
		return line.replace('??{}??'.format(variable), eval('self.{}'.format(variable)))
