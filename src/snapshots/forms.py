from django import forms

class restoreForm(forms.Form):
	restorePath = forms.CharField(label='Path to restore backup (on this system): ', max_length=32)