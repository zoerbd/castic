#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo 'En1}AGN5nQRu,CXg[>VGjvkS@LTDw4navvt|j)hYg7.@+`FzhRTe0mEVN=V}P_xQFOb}5mVswQXDib)}>*L-vZpp9L0:IJ8J)iWlJ*a;GZ9}jLHe:S-a7QT<1FHgQRxh' > /etc/restic.pw
chmod 600 /etc/restic.pw

# generate key if not existing
if ! [ -e ~/.ssh/id_rsa.pub ]; then
	ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' >> /dev/null 2>&1
fi

chmod 600 ~/.ssh/id_rsa*
sshpass -f /etc/restic.pw ssh-copy-id restic@"teching.dev" >> /dev/null 2>&1

# init repo and backup
restic -r sftp:"teching.dev":"/var/www/castic/awaoj" init --password-file /etc/restic.pw
restic -r sftp:"teching.dev":"/var/www/castic/awaoj" backup "/" --password-file /etc/restic.pw
