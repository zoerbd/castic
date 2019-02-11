from django.shortcuts import render, redirect
import bcrypt
from .forms import loginForm
from .models import login

# Create your views here.
def login(request):
	'''
	Login backend logic
	'''
	if request.method == 'POST':
		form = loginForm(request.POST)
		if form.is_valid():
			if __checkLogin__(form['username'], form['password']):
				redirect('/')
	else:
		form = loginForm()
	return render(request, 'login.html', {'form' : form})


def __checkLogin__(user, pw):
	'''
	Verify user login
	'''
	col = login.objects.get(username=user)
	if not col:
		return False
	return bcrypt.checkpw(pw.encode('utf-8'), col.values()['password'])		# don't know if this shit works