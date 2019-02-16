#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo "G;L3t:y,?xu;<uQ5CF:wut+f6<}vqTPo:N>ez^N|o0BBat\|l8?Mk9jO{=huI]ZRf+UE:3@qk*s-b<-AT1e4oF8bm0[`^Vo^mly5C[q2:_?J`Zb@VET7)lK,CJilcJu3" > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' >> /dev/null 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -f /etc/restic.pw ssh-copy-id restic@"zoerb.cc
" >> /dev/null 2>&1

# init repo and backup
restic -r sftp:"zoerb.cc
":"/var/backup/" init --password-file /etc/restic.pw
restic -r sftp:"zoerb.cc
":"/var/backup/" backup "/etc/" --password-file /etc/restic.pw
