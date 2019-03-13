#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo 'cNKsVsJ;5a7C?8^+rTf{mt@@}8}Ax<1*T/6fxT+)vaL,UZc,ElF)eM7Gw.FIRKi@NGNw65G+=eF6Hn[dxsN_0S]fr29fc-8+P.C;k=q:8/,,xol[j)cl=i@VVRfkkWuH' > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' >> /dev/null 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -f /etc/restic.pw ssh-copy-id restic@"teching.dev" >> /dev/null 2>&1

# init repo and backup
restic -r sftp:"teching.dev":"/var/www/castic/zoerb" init --password-file /etc/restic.pw
restic -r sftp:"teching.dev":"/var/www/castic/zoerb" backup "/" --password-file /etc/restic.pw
