========
castic - docs
========

|

Features
----------------------

Castic features the most common things you would expect a backup system to do.
Here is an short overview:
	information:
		-> shows overall server information such as available disk space on used partition
		-> lists for each repository important information such as space it takes, date of last check and of course the health status
		-> enables you to take a look at any snapshot you took (including restore and delete options)
		-> automated checks and mail-notifications
	Integrate:
		-> has ansible backend to include new remote systems via ssh

|

Building and Setup without installer
----------------------

Warning: a debian based system is used for the following steps, but for other systems, the packages and paths should be named similar.

|

Install requirements and dependencies
########

At the beginning you have to install some dependencies.
First of all let's install restic:
Warning: This is the current version of restic at the time when this document was written, so be aware of the possibiltiy of downloading outdated software.

	curl https://github.com/restic/restic/releases/download/v0.9.4/restic_0.9.4_linux_amd64.bz2 --output restic.bz2

	bunzip2 restic.bz2

	sudo mv restic /usr/local/bin/restic

	rm restic.bz2

Next step is to install the packages that are written in requirements.sh:

	cd /path/to/castic/folder

	sudo apt-get install $(cat requirements.sh)

After that we need to make sure that our python dependencies are installed and our virtual environment is set up correctly:

	python3 -m pip install -r requirements.txt

	pipenv shell

	pipenv update

|

setup infrastructure
########

Now we start to setup our deployment infrastructure.
For this app, I will setup gunicorn (WSGI-server) as a systemd service and nginx (high performance reverse-proxy and http-server).
Gunicorn will listen on traffic from localhost:8000 while nginx forwards any traffic on port 80 (you can configure of course https also) to 
the gunicorn instance on port 8000.
I prepared already a systemd service file at src/bin/castic.service which you can modify as you want and copy it to /etc/systemd/system/castic.service.
	
	sudo cp src/bin/castic.service /etc/systemd/system/castic.service

Now we only have to commit small changes to our /etc/nginx/nginx.conf file, simple add or replace this for an existing default server block:

	server {
		listen       80;
		server_name  server.tld;
		root         /var/www/castic;
		include /etc/nginx/default.d/*.conf;
		location /static/ {
			root /var/www/castic/src;
		}
		location / {
			proxy_pass http://unix:/run/gunicorn/socket;
		}
	}

db management
########

As the projects uses SQLite, the DB setup is pretty easy.
Simply make sure to be in the virtual environment (pipenv shell) and type the following commands:

	cd src			# cd into the src folder of the project
	./manage.py makemigrations
	./manage.py migrate


user management
########

Castic has no dedicated management system for it's user, but you should take a look at accessing
your users from commandline.

	./manage.py shell

Then import the necessary database model:

	>>> from django.contrib.auth.models import User
	>>> from getpass import getpass


After that, you can for example create a new user:

	>>> user = User.objects.create_user(username=input('Your username: '), password=getpass())
	>>> user.save()

Exit by typing CTRL + D or exit().

|

configuration file
########

You find a config.json file in the projects source.
It's basically that one place where all user made settings are stored.
It could also be solved by doing that in the database but I personally like it when I have quick and easy commandline 
access to whatever settings I want to alter or review.
But of course you don't have to edit it directly.
The settings tab does nothing but let you set exactly those values that are written in the config.json 
(simply generates new config file each time you submit).

Warning: Please be careful to meet formal requirements when chaning values, because in the current release, there is no strong protection on submit.

|

------------

