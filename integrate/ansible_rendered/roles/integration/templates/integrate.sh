#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo "\TkF3q43Pxl;?.H[U{;J9:P{qxt8pPbZq9OvWKR9QC5NHO[V`VBDM{,\YGIo,0}c9`hOzW2+6]|9Bp\);T*WQ[E`S9L}Ph5OT,<hAjg3m\Hk|jg`pjc,1>/MBQ_1iy;K" > /etc/restic.pw
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
