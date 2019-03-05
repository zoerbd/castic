import re
from castic.globals import config
import smtplib
from repositories.models import repositories
from repositories.views import __getFreeDiskSpace__
from django.utils.timezone import now

class mailingNotification():
	def __init__(self):
		self.config = config['notify']
	
	def manageMailing(self):
		'''
		This method is called from update/views.py after doing update.
		It will check if notifications are enabled, if config from user is valid
		and try to send the notication mail.
		If this method was successful, it returns nothing.
		'''
		if not self.config['sendMailNotifications']:
			return 'Not sending mail, because notifications are disabled in settings.'
		if not self.__checkMailingConfig__():
			return 'Error in config-syntax detected.\nExiting.'
		return self.__renderAndSendMail__()

	def __checkMailingConfig__(self):
		'''
		This method gets called by manageMailing().
		It checks if the config is valid.
		If that's the case, it returns True.
		'''
		# define all used regex-patterns
		mailPattern = re.compile(r'\w+\@[\w+\.\w+|localhost]')
		domainPattern = re.compile(r'^([.*\.\w+|localhost])$')
		sizePattern = re.compile(r'^(\d+[A-Z])$')

		# check if mail addresses are valid
		matches = []
		matches.append(mailPattern.finditer(self.config['mailAddress']))
		matches.append(mailPattern.finditer(self.config['mailFrom']))
		matches.append(domainPattern.finditer(self.config['smtpServer']))
		matches.append(sizePattern.finditer(self.config['warnIfDiskSpaceSmallerThan']))

		# ---------> implement logging here or more verbose output
		for matchgroup in matches:
			if not [match.group(0) for match in matchgroup]:
				return False
		return True

	def __renderAndSendMail__(self, mail):
		'''
		This method gets called by manageMailing().
		It authenticates the user at localhost or remote-end and
		tries to send the previously rendered mail.
		Returns nothing except an error occurred.
		'''
		# //// include these options
		user = self.config['smtpUsername']
		password = self.config['smtpPassword']
		# //// include these options

		content = """From: {}
To: {}
Subject: Castic: Backup information\n
This is a generic mail from your castic server.
I am built to check all backups on certain time periods.\nAvailable disk-space on your backup volume: {}.\n\n""".format(
		self.config['mailFrom'], self.config['mailAddress'], __getFreeDiskSpace__())

		# check if all repos are healthy (fetch data from db). if not, append error message
		errors = [ '{0} - FATAL ERROR: Error was detected in repository \'{1}\'.\nYou should check the repo \
					and verify that the backup is done correctly.'.format(now(), list(repositories.objects.values())[j])
					for j, health in enumerate(repositories.objects.values_list('health')) if health[0] != 1]
		content.append('\n'.join(errors))

		if not errors:
				content.append('All integrated servers were backuped successfully.\nEverything seems clean and healthy.\n\n')
		content.append('Regards,\nyour backup-friend check_backups.py')

		try:
				smtp = smtplib.SMTP(self.config['smtpServer'])
				smtp.sendmail(
					self.config['mailFrom'], 
					[self.config['mailAddress']], 
					content
				)
		except Exception as err:
				return __log__(' <--SMTP--> ERROR OCCURED WHILE TRYING TO SEND MAIL: {}\n'.format(err))