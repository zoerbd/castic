#!/bin/bash

# make sure ~/.ssh directory exists
if ! [ -d ~/.ssh ];then
	mkdir ~/.ssh >> $log 2>&1 
fi

# set right permissions
chmod 600 ~/.ssh

# setup password-free ssh
echo '5O\yu]F9d*kRUn^/oZ>Y,*K|)x/=Okve`J)Ca[wC`Fg5jr>227Eum5P/q|1cAs7QBM=CakXjnKlD1|\e)nl)xp)O1MUnq?,2JDm^9O0Z8Nm57Z?g{uh_/hrLb.7I@MSB' > /etc/restic.pw
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
