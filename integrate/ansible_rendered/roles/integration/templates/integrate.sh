#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo '{W+}4^3zyW]G,+4kk{ayt}>2rS^=RFrgz,@WA?UeH=]+Elkv`yRQ_hDXi@p^<eLW}5vU10rKfL+C4]LGpqIbR`=73Ypzm|}[J0aJ?Bc9=6knyO<_j@Xa*T0,)ZiG7zmE' > /etc/restic.pw
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
