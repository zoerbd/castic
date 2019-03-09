#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo ',)xUIo5V`=q?bRVyYC5g/E:q8dSC4Mnc\IT5sl=<902N5pI<3Bc<]M61pCI_)?UF?Q>?fIGN<Fu_y<G0P+s9S+o>;Kwm)9Tzr@2pIcL-eio:sE;;CL1>/)`U`eP]M=c8' > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' >> /dev/null 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -f /etc/restic.pw ssh-copy-id restic@"teching.dev" >> /dev/null 2>&1

# init repo and backup
restic -r sftp:"teching.dev":"clear" init --password-file /etc/restic.pw
restic -r sftp:"teching.dev":"clear" backup "ls -la" --password-file /etc/restic.pw
