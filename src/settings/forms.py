from django import forms

class settingsForm(forms.Form):
	# general
	backupPath = forms.CharField(label='Backup path', max_length=32)
	autoForgetAll = forms.CharField(label='Number of snapshots to keep on all repos', max_length=32)

	# check
	DoCheckInBackground = forms.CharField(label='Check backups in background', max_length=32)
	autoCheck = forms.CharField(label='Auto check', max_length=32)
	executeCommandAfterCheck = forms.CharField(label='Execute command after check', max_length=32, required=False)

	# notify
	mailAddress = forms.CharField(label='Mail-address', max_length=32)
	sendMailNotifications = forms.CharField(label='Send notifications via mail', max_length=32)
	warnIfDiskSpaceSmallerThan = forms.CharField(label='Warn if disk space smaller than', max_length=32)
	mailFrom = forms.CharField(label='Mail from', max_length=32)
	smtpServer = forms.CharField(label='SMTP-server', max_length=32)
	smtpUsername = forms.CharField(label='SMTP-user', max_length=32, required=False)
	smtpPassword = forms.CharField(label='SMTP-password', widget=forms.PasswordInput(), required=False)