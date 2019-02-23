========
castic - docs
========
------------
Building
----------------------
You have several options to build the package.
The easiest one is to do the following:

	1. Change directory to wherever you have the directory, including this file.
	2. Just execute the basic setup with: ```pip install -e .```
	3. Recommended: Optionally if you want a full setup to be created by an interactive installer, run this command: ```src/bin/installme.py```

Otherwise you can also simply execute the setup.py-file.
But I would strongly recommend to use the src/bin/installme.py script for installation process.
It helps you creating a user, migrating the required database and setting up your webserver infrastructure.
**WARNING: The installme-script is currently only available for CentOS-systems. So you have to do some stuff manually but more later on.**


Features
----------------------
Castic features the common things you would want to do with a backup system.
Here is an short overview:
	information:
		-> shows overall server information such as available disk space on used partition, ...
		-> lists for each repository important information such as space it takes, date of last check and of course the health status
		-> enables you to take a look at any snapshot you took (including restore and delete options)
	Integrate:
		-> has ansible backend to include new remote systems via sftp
	Misc:
		-> automated checks and mail-notifications
------------