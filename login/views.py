from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as djangoLogin
from .forms import loginForm

# Create your views here.
def login(request):
	'''
	Login backend logic
	'''
	if request.method == 'POST':
		form = loginForm(request.POST)
		if form.is_valid():
			if authenticate(username=form['name'].value(), password=form['password'].value()) is not None:
				djangoLogin(request, user)
				return redirect('/')
		return redirect('http://duckduckgo.com/invalid-login')
	else:
		form = loginForm()
	return render(request, 'login.html', {'form' : form})
