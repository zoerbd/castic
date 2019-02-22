#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo 'sXv_2WzQX>FL@B{SHWcw7|1Gt=z[Y:7-=J,lf2dy_Rzl8go}rO|lZmKWO,yr?EqOdtpm?7iL@V1d.__YpYr.d-|`Mx;,oU|T,2=m80{KC:3=R;fBE}*M}m4g[uDr+ePM' > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' >> /dev/null 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -f /etc/restic.pw ssh-copy-id restic@"zoerb.cc" >> /dev/null 2>&1

# init repo and backup
restic -r sftp:"zoerb.cc":"zoerb" init --password-file /etc/restic.pw
restic -r sftp:"zoerb.cc":"zoerb" backup "/etc" --password-file /etc/restic.pw
