from django import forms

class integrateInformation(forms.Form):
	# ordinary text input
	user = forms.CharField(label='Remote-user', max_length=32)
	localUser = forms.CharField(label='User on local castic server', max_length=32)
	localUser = forms.CharField(label='User on local castic server', max_length=64) 
	dest = forms.CharField(label='dest', max_length=64)
	repoPath = forms.CharField(label='repoPath', max_length=32)
	backupPath = forms.CharField(label='backupPath', max_length=32)

	# passwords
	password = forms.CharField(widget=forms.PasswordInput())
