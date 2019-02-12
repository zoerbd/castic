from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import loginForm

# Create your views here.
def login(request):
	'''
	Login backend logic
	'''
	if request.method == 'POST':
		form = loginForm(request.POST)
		if form.is_valid():
			if authenticate(username=form['name'], password=form['password']):
				redirect('/')
	else:
		form = loginForm()
	return render(request, 'login.html', {'form' : form})
