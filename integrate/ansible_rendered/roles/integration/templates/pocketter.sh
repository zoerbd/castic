#!/bin/bash

#///////////////////////////////////////////////////////////////////
#<------------------------|default values|------------------------>
log="./pocketter.log"

# destination system
dhost="example.tld"
# backup type (sftp, local, (rest))
dtype="sftp"
# repository to store snapshots
drepo="/var/backup"
# path to backup to $drepo
dbackup="/etc"

dcronjob="0 0 * * * restic -r $drepo forget --keep-last 3 --prune"
cron_path="/etc/crontab"
#<---------------------------------------------------------------->
#//////////////////////////////////////////////////////////////////

# color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

# list of available parameter
parameter_list=( 
	"install"
	"-h"
	"-d"
	"-i"
	"-f"
	"-fd"
	"-p"
	"-t"
)

# list of parameter description
parameter_description=( 
	"\tinstall\t\t\t\t-> install restic"
	"\t-h\t\t\t\t-> here you are :)" 
	"\t-d\t\t\t\t-> work with default values on top of this script"
	"\t-i\t\t\t\t-> interactive config (use only this if your new to this)" 
	"\t-f\t\t\t\t-> set up cronjob to forget automatically"
	"\t-fd\t\t\t\t-> set up cronjob to forget automatically (using default values)"
	"\t-p\t\t\t\t-> print documentation"
	"\n\t-t <type> <user@destination> <repository> <backup-path> -> start backup non-interactive\n\t*for local backups only call ./pocketter.sh -t local <local-repo> <backup-path>"
)


# list of parameter function names
parameter_func=( 
	"install"
	"help" 
	"start_default"
	"start_interactive" 
	"automatic_forget"
	"default_automatic_forget"
	"print_docs"
	"set_type"
)

#---------------------------------------------------------------------------------------

# print help
function help(){
	echo -e "\nUsage: ./pocketter.sh <options>\n\n"
	echo -e "Available options: "

	# print any parameter description
	i=0
	while [ $i -lt ${#parameter_description[*]} ]; do
		echo -e "${parameter_description[i]}"
		i=$((i + 1))
	done
	echo -e "\n\n\nAvailable backup types:\n\t-> sftp\n\t-> local\n\t-> rest\n"
}

function sysd(){
	#echo -e "$(date +%F" "%T): Last command: !! " >> $log 2>&1
	# if last executed command returned with 0
	if [ "$?" == 0 ]; then
		echo -e "[ ${GREEN} OK ${NC} ] $1"
		echo -e "$(date +%F" "%T):  $1" >> $log 2>&1
	else
		echo -e "[ ${RED} !! ${NC} ] $2"
		echo -e "$(date +%F" "%T):  $2" >> $log 2>&1
	fi
}

function install(){
	# check if git is installed
	git --help >> /dev/null 2>&1
	sysd "Checked git, start downloading..." "Could not start git"
	
	# try to clone from github
	git clone https://github.com/restic/restic >> /dev/null 2>&1
	sysd "Successfully cloned from Github" "Could not clone from Github, now trying local repo"
	
	# git clone ssh://user@host/path/to/repo >> /dev/null 2>&1
	# sysd "Successfully cloned from local repository" "Could not clone from local repo"
	
	cd ./restic

	# build executable
	go run build.go
	sysd "Built executable" "Error occurred while building executable, check go compiler"

	cd ..

	# install to /usr/bin
	mv ./restic/restic /usr/bin/restic
	sysd "Successfully installed to /usr/bin/restic" "Error occurred while installing to /usr/bin/"
	
	# check if restic is accessable
	restic -h >> /dev/null 2>&1
	sysd "Tested compiled program" "Error testing restic"
}

function print_docs(){
echo -e "

Overview:
------------------------------------------------------------

Initialize repository at /var/backup\t\t\t-> restic -r /var/backup init

Initialize remote-repository at /var/backup\t\t-> restic -r sftp:user@host:/var/backup init

Backup data from /home/user to /var/backup\t\t-> restic -r /var/backup backup /home/user (optional: --passwordfile pass.txt; --tag \$tag; --exclude="\$file")

Show backup (snapshot) info\t\t\t\t-> restic -r /var/backup snapshots

Show difference between two snapshots\t\t\t-> restic -r /var/backup diff \$snapshot_id1 \$snapshot_id2

Remove snapshot (does not fully delete)\t\t\t-> restic -r /var/backup forget \$snapshot_id

Search for unnecessary data and delete them\t\t-> restic -r /var/backup prune

Restore backup to /home/user\t\t\t\t-> restic -r /var/backup restore \$snapshot_id --target /home/user (optional: ...restore latest...)

Mount snapshot to /mnt using FUSE\t\t\t-> restic -r /var/backup mount /mnt

"
}


function sftp_setup(){
	# ~/.ssh directory management
	if ! [ -d ~/.ssh ];then
		mkdir ~/.ssh >> $log 2>&1 
		sysd "Created directory ~/.ssh" "Could not create ~/.ssh"
	elif [ -e ~/.ssh/id_rsa.pub ];then
		# ------------------------------------------------------> Use carefully because of other dependencies
		rm ~/.ssh/id_rsa* >> $log 2>&1
	fi

	# check input
	[ -z "$1" ] && echo "${RED}user@host is not given...Exiting${NC}"
	[ -z "$2" ] && echo "${RED}repository path is not given...Exiting${NC}"
	[ -z "$3" ] && echo "${RED}backup path is not given...Exiting${NC}"

	# set right permissions
	chmod 600 ~/.ssh
	
	# make pubkey
	echo "Enter password for generating ssh-key: "
	ssh-keygen -f ~/.ssh/id_rsa >> /dev/null 2>&1
	sysd "Created ssh-key for authentication" "Error occurred generating ssh-key for authentication"

	# set right permissions to keys
	chmod 600 ~/.ssh/id_rsa*

	# start preparing server
	echo "Connect to remote host: "
	ssh-copy-id "$1" >> /dev/null 2>&1
	sysd "Server successfully prepared for authentication with certificate" "Error preparing server"

	# connect to remote-side and exec exit
	ssh "$1" exit >> $log 2>&1
	sysd "Tested connection" "Error testing connection."
	
	# check if restic is installed
	restic >> /dev/null 2>&1 
	sysd "restic is accessable" "restic maybe not installed yet."
	
	# initialize remote repo
	restic -r sftp:"$1":"$2" init
	sysd "Successfully initialized restic repository on remote host." "Error occurred while trying to initialize restic repository on remote host."

	# print warning and do init backup
	echo -e "${RED}WARNING: Now an initial backup will be done, to make sure that everything works.\nTo stop just hit CTRL + C, at this point everything was successfully prepared.${NC}"
	echo -e "Starting backup ..."
	restic -r sftp:"$1":"$2" backup "$3" 
	sysd "Successfully tested backup to remote repository." "Error occured while trying to backup to remote repository"

	sysd "Everything successfully prepared"
	exit
}


function local_setup(){
	# init local repo
	restic -r "$1" init
	sysd "Successfully initialized local repository" "Error occured initializing local repository"

	# do init backup
	echo "Starting backup to verify functionality..."
	restic -r "$1" backup "$2"
	sysd "Successfully backuped" "Error occurred while trying to backup"
	exit
}


function rest_setup(){
	echo "Maybe coming soon!" && exit
}

function set_type(){
	# initialize setup process with additional parameter
	[  "$2" == "sftp" ] && sftp_setup "$3" "$4" "$5"
	[  "$2" == "local" ] && local_setup "$3" "$4"
	[  "$2" == "rest" ] && rest_setup "$3" "$4" "$5"
}

# start processing with default values
function start_default(){
	set_type "-d" "$dtype" "$dhost" "$drepo" "$dbackup"
}

# set up cronjobs for automation in forget processes (with default values)
function default_automatic_forget(){
	echo "$dcronjob" >> $cron_path
}

# set up cronjobs for automation in forget processes
function automatic_forget(){
	echo -e "${RED}WARNING: This option is in experimental state of development!${NC}"
	
	# ask many questions to setup forget rule and write to crontab file
	read -p "According to which selection criteria? [time/tag/number] " ftype
	read -p "How often do you want to execute cronjob? (input cronjob time-code) " fcrontime
	read -p "Path to affected repository: " frepo
	read -p "Do you want to prune after forgetting? (this is necessary to delete completely) [y/n]
" fprune

	if [ "$ftype" == "time" ]; then
		read -p "According to which time unit? [hour/day/week/month/year] " ftime
		read -p "Keep snapshots of last __ "$ftime"s " fnum
		echo "$fcrontime restic -r $frepo forget --keep_"$ftime"ly $fnum" >> $cron_path

	elif [ "$ftype" == "tag" ]; then
		read -p "Keep all snapshots which have all tags specified by this (can be specified multiple times): " ftag
		echo "$fcrontime restic -r $frepo forget --keep-tag $ftag" >> $cron_path

	elif [ "$ftype" == "number" ]; then
		read -p "Never delete the (most recent) ___ last snapshots: " fnum
		echo "$fcrontime restic -r $frepo forget --keep-last $fnum" >> $cron_path

	else
		echo "Got no input.\nExiting!" && exit
	fi

	[ "$fprune" == "y" ] && echo "restic -r $frepo prune" >> $cron_path
	echo "done"
}

# start in interactive mode
function start_interactive(){
	read -p "Where should be backuped to? (remote, local) " rdest
	if [ "$rdest" == "remote" ]; then
		read -p "backup-type (sftp, rest): " rtype 
		read -p "user@server: " rhost
		read -p "Path to store backups (at remote host): " rdir
	elif [ "$rdest" == "local" ]; then
		read -p "Path to store backups: " rdir
	else	
		exit
	fi
	read -p "Path to backup: " rback
	set_type "-i" "$rtype" "$rhost" "$rdir" "$rback"
}

#----------------------------------------------------------------------------------------

# while i smaller than num of available parameter
i=0
while [ $i -lt ${#parameter_list[*]} ]; do

	# if parameter from list is choosen execute parameters function
	[ "$1" == ${parameter_list[i]} ] && eval ${parameter_func[i]} $* && exit
	i=$((i + 1))
done

# if non option choosen script is not correctly handled
help
