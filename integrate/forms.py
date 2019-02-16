from django import forms

class integrateInformation(forms.Form):
	user = forms.CharField(label='Remote-user', max_length=16)
	password = forms.CharField(widget=forms.PasswordInput())
	dest = forms.CharField(label='dest', max_length=16)
	resticPassword = forms.CharField(widget=forms.PasswordInput())
	repoPath = forms.CharField(label='repoPath', max_length=16)
	#forms.BooleanField(required=False)
