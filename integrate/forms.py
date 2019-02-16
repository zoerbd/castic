from django import forms

class integrateInformation(forms.Form):
	# ordinary text input
	user = forms.CharField(label='Remote-user', max_length=16)
	dest = forms.CharField(label='dest', max_length=16)
	repoPath = forms.CharField(label='repoPath', max_length=16)
	backupPath = forms.CharField(label='backupPath', max_length=16)

	# passwords
	password = forms.CharField(widget=forms.PasswordInput())
	#resticPassword = forms.CharField(widget=forms.PasswordInput())

	# check boxes
	ownPassword = forms.BooleanField(required=False)
