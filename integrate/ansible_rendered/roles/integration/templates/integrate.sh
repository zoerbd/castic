#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo "Z`E*ghdAXT+HYN>1tA}.{Tf1g;q/V3t`@y@LT=0}1P1MG2?\vEGUmy?S[}n/FQ\-LXY*V?kcsNoQKa`giEJKD=bO.ARDAncD;Seo`jx7s55Jq9y@YOO5,t?)IT0OLUps" > /etc/restic.pw
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
