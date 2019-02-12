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
				return redirect('http://zoerb.cc:8080/')
		return redirect('http://duckduckgo.com/unallowed-access')
	else:
		form = loginForm()
	return render(request, 'login.html', {'form' : form})
