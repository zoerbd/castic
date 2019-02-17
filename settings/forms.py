from django import forms

class settingsForm(forms.Form):
	# general
	backupPath = forms.CharField(label='backup path', max_length=32)

	# check
	DoCheckInBackground = forms.CharField(label='', max_length=32)
	checkMode = forms.CharField(label='', max_length=32)
	autoCheck = forms.CharField(label='', max_length=32)
	executeCommandAfterCheck = forms.CharField(label='', max_length=32)

	# notify
	mailAddress = forms.CharField(label='', max_length=32)
	sendMailNotifications = forms.CharField(label='', max_length=32)
	warnIfDiskSpaceSmallerThan = forms.CharField(label='', max_length=32)
	mailFrom = forms.CharField(label='', max_length=32)
	smtpServer = forms.CharField(label='', max_length=32)
	smtpUsername = forms.CharField(label='', max_length=32)
	smtpPassword = forms.CharField(widget=forms.PasswordInput())