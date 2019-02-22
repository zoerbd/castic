#!/usr/bin/env python3
from setuptools import setup, find_packages
from setuptools.command.install import install
from webmanagement.settings import __shell__, getVersion
from webmanagement.installme import setupDependencies

class Installer(install):
	def run(self):
		install.run(self)
		print(setupDependencies().startSetup())
	
cmdclass={'install':Installer}

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
	packages = find_packages(), #exclude=['*.md', '*.log', '*.log', 'Pipfile*', '\.*', 'config*', 'Docker*', 'requirements*']),
	iclude_package_data = True,
	zip_safe = False,
	classifiers = [
		'Environment :: Web Environment',
		'Operating System :: POSIX',
		'Programming Language :: Python',
		'Topic :: Internet :: WWW/HTTP',
        'Framework :: Django'
	],
	install_requires = open('requirements.txt').read(),
	scripts = ['manage.py']
)
