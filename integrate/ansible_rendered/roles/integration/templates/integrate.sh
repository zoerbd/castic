#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo 'fumdMJdEgaO@ihWjV6s|?cOGSnMS8vFXDMAC=g)]WI1-VF:B*XL;rFYD@ZU[iI<3)OQSq.Ghkh^4,a6G+I?4W9PIT5VAwBjx-v/pQbR29@L1SyG|*3:fhy7L+=\FCqF+' > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' >> /dev/null 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -f /etc/restic.pw ssh-copy-id restic@"zoerb.cc" >> /dev/null 2>&1

# init repo and backup
restic -r sftp:"zoerb.cc":"/var/backup/repo" init --password-file /etc/restic.pw
restic -r sftp:"zoerb.cc":"/var/backup/repo" backup "/etc/" --password-file /etc/restic.pw
