#!/usr/bin/env python3
'''
This script is made to be called from setup.py file.
'''

from settings import __shell__, __log__
from django.contrib.auth.models import User
from getpass import getpass

class setupDependencies:
	def __init__(self, *args, **kwargs):
		pass

	def startSetup(self):
		'''
		Setup for production.
		'''
		if not self.__ask__('Start interactive setup for your webserver-environment?'):
			return __log__('Exited because setup is not wished.')
		self.__installOSPackages__()

		# setup database
		dbSetups = {
			'mysql':'self.__mysqlSetup__()',
			'sqllite':'self.__sqlliteSetup__()',
			'postgres':'self.__postgresSetup__()'
		}
		dbSetupOption = self.__ask__('Which database should be used for backend?', '[\'MySQL\'|\'SQLLite\'|\'Postgres\']')
		if dbSetupOption:
			result = eval(dbSetups[dbSetupOption])
			if not result:
				return __log__('Error occurred while trying to setup database: {}'.format(result))
			[ __log__('Database migration returned with: {}'.format(__shell__(command))) 
			  for command in ['../manage.py makemigrations', '../manage.py migrate'] ]
		
		# setup user
		print('Create user for authenticate for castic webmanagement.')
		user = User.objects.create_user(username=input('Username: '), password=getpass())
		user.save()

		# setup webserver infrastructure
		webInfastruct = self.__ask__('Which webserver infrastructure do you want to setup? \
		\n  a) gunicorn + nginx reverse proxy (recommended)\n  b) apache2 + mod_wsgi\
		\n  c) Docker (for testing in an isolated virtual environment)', '[\'a\'|\'b\'|\'c\']')
		webInfrastructures = {
			'a':'self.__gunicornSetup__()',
			'b':'self.__apacheSetup__()',
			'c':'self.__dockerSetup__()'
		}
		if not webInfastruct:
			return __log__('Error occurred while trying to setup database: {}.'.format(webInfastruct))
		eval(webInfrastructures(webInfastruct))

	def __mysqlSetup__(self):
		return False
	
	def __sqlliteSetup__(self):	
		return False

	def __postgresSetup__(self):
		return False

	def __gunicornSetup__(self):
		return False

	def __apacheSetup__(self):
		return False

	def __dockerSetup__(self):
		return False

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
		return [__shell__('yum install {}'.format(package)) for package in open('../requirements.sh').readlines()]	# only CentOS Support

if __name__ == '__main__':
	print(setup().startSetup())