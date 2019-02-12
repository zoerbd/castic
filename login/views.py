from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
import bcrypt
from .forms import loginForm

# Create your views here.
def login(request):
	'''
	Login backend logic
	'''
	if request.method == 'POST':
		form = loginForm(request.POST)
		if form.is_valid():
			if authenticate(form['username'], form['password']):
				redirect('/')
	else:
		form = loginForm()
	return render(request, 'login.html', {'form' : form})


def __checkLogin__(user, pw):
	'''
	Verify user login
	'''
	col = passwd.objects.get(username=user)
	if not col:
		return False
	return bcrypt.checkpw(pw.encode('utf-8'), col.values()['password'])		# don't know if this shit works