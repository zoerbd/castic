#!/usr/bin/env python3
from setuptools import setup, find_packages
from src.castic.globals import __shell__, getVersion
from src.bin.installme import setupDependencies

setup(
	name = 'castic',
	version = getVersion(),
	description = 'A webmanagement built on the top of the non-graphical open-source backup program \'restic\'.',
	long_description = open('README.md').read(),
	author = 'Dominic Zoerb',
	author_email = 'dominic.zoerb@gmail.com',
	license = 'GPL3',
	url = 'https://bitbucket.org/zoerbd/castic',
	download_url = 'https://bitbucket.org/zoerbd/castic',
	packages = find_packages(), 
	include_package_data = True,
	zip_safe = False,
	classifiers = [
		'Environment :: Web Environment',
		'Operating System :: POSIX',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP',
	        'Framework :: Django'
	],
	install_requires = open('requirements.txt').read(),
	scripts = ['src/manage.py']
)

# try to execute installme-script
try:
	setupDependencies().startSetup()
except:
	print('////////')
	print(' For full setup that includes user creation, database-migration, webserver-infrastructure and more, execute >>>src/bin/installme.py<<<')
	print('////////')