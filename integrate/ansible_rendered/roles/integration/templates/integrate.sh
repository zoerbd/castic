#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo "0rdcF;Lc_q8X]jy}j]Eg[58yw:wn1[P;1c.[}kxM7Fd1E:.Kv.R`exIH*fLaYA]=5}m5A,w1erkC,1Q,b^Ia<)+]R2akdfJ,FxwOIfr?2s>r^kG2}S,aOXmi\e;k]w<:" > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' >> /dev/null 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -f /etc/restic.pw ssh-copy-id restic@"zoerb.cc
" >> /dev/null 2>&1

# init repo and backup
restic -r sftp:"??ownHost??":"/var/backup/" init --password-file /etc/restic.pw
restic -r sftp:"??ownHost??":"??repoPath??" backup "/etc/" --password-file /etc/restic.pw
