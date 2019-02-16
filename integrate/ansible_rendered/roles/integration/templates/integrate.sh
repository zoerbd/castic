#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo "riEn;qf7>0fbE^,wAYOtYrTgfOMwH@}q>cXTz2ylrgKrb^-qyLikGikSXI0c5SAtk1*=B3|ez:XR@<Z\Kh[^qc_FcCNmx,z1t;;wjn]/9isxo>2=.DNsFX)@n-:/Ww.B" > /etc/restic.pw
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
