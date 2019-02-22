from django import forms

class loginForm(forms.Form):
	name = forms.CharField(label='Username', max_length=16)
	password = forms.CharField(widget=forms.PasswordInput())
