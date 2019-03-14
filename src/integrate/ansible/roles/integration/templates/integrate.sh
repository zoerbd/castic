#!/bin/bash

# make sure ~/.ssh directory exists
unset HISTFILE
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo '??resticPW??' > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -p "??localPassword??" ssh-copy-id ??localUser??@??ownHost?? 2>&1

# init repo and backup
restic -r sftp:??user??@??ownHost??:??repoPath?? init --password-file /etc/restic.pw
restic -r sftp:??user??@??ownHost??:??repoPath?? backup ??backupPath?? --password-file /etc/restic.pw
set HISTFILE
