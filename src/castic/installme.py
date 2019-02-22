#!/usr/bin/env python3
'''
This script is made to be called from setup.py file.
'''
import pdb

from globals import __shell__, __log__
from settings import BASE_DIR
import sys, os

sys.path.insert(0, os.path.join(BASE_DIR))
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
		if int(__shell__('id -u')) != 0:
			return __log__('Exiting: script has to be executed as root!')
		if not self.__ask__('Start interactive setup for your webserver-environment?'):
			return __log__('Exited because setup is not wished.')
		self.__installOSPackages__()

		# setup database
		dbSetups = {
			'a':'self.__mysqlSetup__()',
			'b':'self.__sqlliteSetup__()',
			'c':'self.__postgresSetup__()'
		}
		dbSetupOption = self.__ask__('Which database should be used for backend?\n  a) MySQL\n  b) SQLLite\
		\n  c) Postgres\n ', '[\'a\'|\'b\'|\'c\']')
		if dbSetupOption:
			result = eval(dbSetups[dbSetupOption])
			if not result:
				return __log__('Error occurred while trying to setup database: {}'.format(result))
			[ __log__('Database migration returned with: {}'.format(__shell__(command)))
			  for command in ['./manage.py makemigrations', './manage.py migrate'] ]
		
		# setup user
		print('Create user for authenticate for castic webmanagement.')
		user = User.objects.create_user(username=input('Username: '), password=getpass())
		user.save()

		# setup webserver infrastructure
		webInfastruct = self.__ask__('Which webserver infrastructure do you want to setup? \
		\n  a) gunicorn + nginx reverse proxy (recommended)\n  b) apache2 + mod_wsgi\
		\n  c) Docker (for testing in an isolated virtual environment)\n  ', '[\'a\'|\'b\'|\'c\']')
		webInfrastructures = {
			'a':'self.__gunicornSetup__()',
			'b':'self.__apacheSetup__()',
			'c':'self.__dockerSetup__()'
		}
		if not webInfastruct:
			return __log__('Error occurred while trying to setup database: {}.'.format(webInfastruct))
		# ----------------
		# ////// getting error here: 
		# ------> TypeError: 'dict' object is not callable
		result = eval(webInfrastructures(webInfastruct))
		# //////
		# ----------------
		if not result:
			return __log__('Error occurred while trying to setup webserver infrastructure: {}.'.format(result))

	def __mysqlSetup__(self):
		return True
	
	def __sqlliteSetup__(self):	
		return True

	def __postgresSetup__(self):
		return True

	def __gunicornSetup__(self):
		return True

	def __apacheSetup__(self):
		return True 

	def __dockerSetup__(self):
		return True 

	def __ask__(self, *args):
		'''
		Ask question and return bool answer.
		'''
		if len(args) == 1:
			return __shell__('read -s -n 1 -p "{} [y|n]\n" a && echo $a'.format(args[0])).lower() in ['y', 'yes']

		# do this if options-block (i.e. [y|n|d]) explicitly given and check if answer valid
		question = input('{} {}'.format(args[0], args[1])).lower()
		if not question in [entry.lower() for entry in eval(args[1].replace('|', ','))]:
			return False
		return question
	
	def __installOSPackages__(self):
		'''
		Install requirements for OS that are written in requirements.sh
		'''
		return [ __shell__('yum -y install {}'.format(package)) 
				 for package in open('../requirements.sh').readlines() ]	# only CentOS Support

if __name__ == '__main__':
	setupDependencies().startSetup()
