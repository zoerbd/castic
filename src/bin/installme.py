#!/usr/bin/env python3
'''
This script is made to be called from setup.py file.
'''
import pdb
import sys, os, shutil, json

sourcePath = '/var/www/castic/'
sourcePath = input('Path to the castic source folder (default: /var/www/castic/): ')
sys.path.insert(0, os.path.join(sourcePath, 'src/castic'))
from settings import BASE_DIR

sys.path.insert(0, os.path.join(BASE_DIR))
from globals import __shell__, __log__, gitProjectDir
from django.conf import settings
from django import setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "castic.settings")
setup()

from django.contrib.auth.models import User
from getpass import getpass

class setupDependencies:
	def startSetup(self):
		'''
		Setup for production.
		'''
		print('///--\nWARNING: Make sure to run this script in an existing pipenv.\nDo this by executing the following commands:\n  >> pipenv shell <<\n  >> pipenv update <<\n  >> src/bin/installme.py <<\n///--')

		# chec if user is root
		if int(__shell__('id -u')) != 0:
			return __log__('Exiting: script has to be executed as root!')
		if not self.__ask__('Start interactive setup for your webserver-environment?'):
			return __log__('Exited because setup is not wished.')
		
		# check if os supported
		if __shell__('cat /etc/os-release | grep PRETTY_NAME | cut -d \'=\' -f 2 | cut -d \' \' -f 1 | cut -d \'"\' -f 2') != 'CentOS':
			__log__('Sorry but at the moment, only CentOS systems are supported for the full setup!\nSo you have to manage package installation and webserver infrastructure by yourself.\nContinuing with a basic setup.')
		else:
			self.__OSSpecificSetup__()

		self.__generalSetup__()
		
		# initial backup
		if self.__ask__('Should an initial backup check be done?\nWARNING: To access your repositories, create in your the passwords folder of your castic root directory for each repo a file with its name which contains the password'):
			from update.check import checkRepositories
			checkRepositories()

	def __OSSpecificSetup__(self):
		'''
		This is the part of the setup that is only available on CentOS systems.
		'''
		self.__installDependencies__(open(os.path.join(gitProjectDir, 'requirements.sh')).readlines())

		# setup webserver infrastructure
		webInfastruct = self.__ask__('Which webserver infrastructure do you want to setup? \
		\n  a) gunicorn + nginx reverse proxy (recommended)\
		\n  b) Docker (Use this for testing purposes in an isolated virtual environment)\n  ', '[\'a\'|\'b\']')
		webInfrastructures = {
			'a':'self.__productionSetup__()',
			'b':'self.__dockerSetup__()'
		}
		if not webInfastruct:
			return __log__('Error occurred while trying to setup database: {}.'.format(webInfastruct))

		result = eval(webInfrastructures[webInfastruct])
		__log__('setup for webserver infrastructure returned with: {}.'.format(result))


	def __generalSetup__(self):
		'''
		This is the part of the setup that is available on any system.
		'''
		# setup (migrate) database
		manageExecutable = os.path.join(BASE_DIR, 'manage.py')
		[ __shell__(command, old=True)
		  for command in [ '{} makemigrations'.format(manageExecutable), '{}  migrate'.format(manageExecutable)]]
		
		# setup user
		print('Creating user for authenticate for castic webmanagement.')
		user = User.objects.create_user(username=input('Username: '), password=getpass())
		user.save()

		# install restic
		if self.__ask__('Should restic be installed?'):
			__shell__('wget https://github.com/restic/restic/releases/download/v0.9.4/restic_0.9.4_linux_amd64.bz2')
			__shell__('bunzip2 restic_0.9.4_linux_amd64.bz2')
			shutil.copyfile('restic_0.9.4_linux_amd64', '/usr/bin/restic')
			__shell__('chmod a+x /usr/bin/restic')
			__shell__('rm -R ./restic_0.9.4_linux_amd64*')

		# backupPath to config
		backupPath = input('Enter the path of your stored repositories: ')
		configFile = os.path.join(gitProjectDir, 'config.json')
		with open(configFile, 'r') as jsonFile:
			data = json.load(jsonFile)
		data['general']['backupPath'] = backupPath
		with open(configFile, 'w') as jsonFile:
			json.dump(data, jsonFile)

	def __productionSetup__(self):
		'''
		This method is called from self.startSetup and 
		manages nginx-reverseProxy/gunicorn production setup.
		'''
		self.__installDependencies__(['nginx'], ['gunicorn'])
		self.__setupNginxReverseProxy__()
		return self.__setupGunicorn__()


	def __setupNginxReverseProxy__(self):
		'''
		This function overwrites the nginx.conf with 
		reverse proxy configuration (localhost:8000) for gunicorn.
		'''
		nginxConfPath = '/etc/nginx/nginx.conf'
		nginxConf = open(nginxConfPath).readlines()
		shutil.copyfile(nginxConfPath, nginxConfPath + '.orig')

		port = 80
		if not self.__ask__('Should port 80 be used for your vHost?'):
			port = int(input('Which port should be used for your vHost? '))
		
		beginHttp = self.__getConfStructure__(nginxConf)
		if len(beginHttp) < 1:
			return __log__('Error occurred while trying to setup nginx: http block not found in /etc/nginx/nginx.conf.')

		vhostConfig = ['server {',
					'\tlisten       {};'.format(str(port)),
					'\tserver_name  {};'.format(__shell__('cat /etc/hostname')),
					'\troot         /var/www/castic;',
					'\tinclude /etc/nginx/default.d/*.conf;',
					'\tlocation /static/ {',
					'\t        root /var/www/castic/src;',
					'\t}',
					'\tlocation / {',
					'\t	proxy_pass http://unix:/run/gunicorn/socket;',
					'\t}',
					'}']

		[nginxConf.insert(beginHttp[0] + 1, line + '\n') for line in reversed(vhostConfig)]
		with open(nginxConfPath, 'w') as outfile:
			outfile.write(''.join(nginxConf))
		return __shell__('systemctl restart nginx')

	def __getConfStructure__(self, conf):
		'''
		This method gets called by self.__setupNginxReverseProxy__.
		It returns a dict that displays the structure of the nginx-config.
		'''
		return [j for j, line in enumerate(conf) if self.__lineIsValid__(['http', '{'], line)]

	def __lineIsValid__(self, tags, line):
		isValid = []
		for tag in tags:
			if '#' in line:
				isValid.append(tag in line and line.index('#') > line.index(tag))
			else:
				isValid.append(tag in line)
		return all(isValid)


	def __setupGunicorn__(self):
		'''
		This function prepares a gunicorn production setup on localhost:8000.
		Based on https://docs.gunicorn.org/en/stable/deploy.html#nginx-configuration.
		'''
		# create gunicorn service 
		systemdDir = '/etc/systemd/system/'
		shutil.copyfile(os.path.join(BASE_DIR, 'bin/gunicorn.service'), os.path.join(systemdDir, 'castic.service'))
		__shell__('systemctl enable gunicorn')
		__shell__('systemctl start gunicorn')


	def __dockerSetup__(self):
		'''
		This method is called from self.startSetup and 
		manages docker isolated testing setup.
		'''		
		self.__installDependencies__(['docker'])
		__shell__('systemctl start docker')
		sys.path.insert(0, gitProjectDir)
		__shell__('docker build -t castic')
		return __log__('Docker setup returned with: {}'.format(__shell__('docker run -it castic')))

	def __ask__(self, *args):
		'''
		Ask question and return bool answer.
		'''
		if len(args) == 1:
                      return input(args[0] + '[y|n]').lower() == 'y'

		# do this if options-block (i.e. [y|n|d]) explicitly given and check if answer valid
		# check one-sized optiosn available to enable using controls without pressing enter
		if all([ True if len(opt.replace('[', '').replace(']', '').replace('\'', '')) == 1 else False for opt in args[1].split('|')]):
                    question = input('{} {}'.format(args[0], args[1].replace('\'', ''))).lower()
		else:
			opt.replace('[', '').replace(']', '').replace('\'', '')

		# check if answer in allowed options
		if not question in [entry.lower() for entry in eval(args[1].replace('|', ','))]:
			return False
		return question

	def __installDependencies__(self, osList, pythonList=None):
		'''
		This method will be called from internal methods that 
		require some OS and python packages to be installed.
		'''
		[__shell__('yum -y install {}'.format(package) for package in osList)]			# only yum support right now
		if pythonList:
			[__shell__('python3 -m pip install {}'.format(package)) for package in pythonList]
	
if __name__ == '__main__':
	setupDependencies().startSetup()
