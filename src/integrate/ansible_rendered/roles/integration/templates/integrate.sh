#!/bin/bash

# make sure ~/.ssh directory exists
unset HISTFILE
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo 'sJLyC?L^5oAB6,`,`]_paK;bFJC[0|2YufDPWZ7/+Lw*5viZHoJ-)*j=<LYUU1W.i{oooIt4F/hjFMS5t_r+4Ku3xc4DD2O+*>VF=1uvUM64m.R9zdl6]d1\[eMJ/Gp<' > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -p "awdawd" ssh-copy-id zod@teching.dev 2>&1

# init repo and backup
restic -r sftp:zod@teching.dev:/var/www/castic/zoerb init --password-file /etc/restic.pw
restic -r sftp:zod@teching.dev:/var/www/castic/zoerb backup / --password-file /etc/restic.pw
set HISTFILE
