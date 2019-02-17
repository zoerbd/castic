import re
from django.core.mail import send_mail
from webmanagement.settings import config

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
		Based on send_mail docs from: https://docs.djangoproject.com/en/2.1/topics/email/
		'''
		return send_mail(
			'Castic: backup status notification',
			'message',
			self.config['mailFrom'],
			[self.config['mailAddress']],
			fail_silently=False,
			auth_user=self.config['smtpUsername'],
			auth_password=self.config['smtpPassword'],
			connection=self.config['smtpServer']
		)