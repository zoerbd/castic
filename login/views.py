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
			if authenticate(username=form['name'].value(), password=form['password'].value()) is not None:
				return redirect('http://zoerb.cc:8080/')
		return redirect('http://duckduckgo.com/{}'.format(form['name'].value()))
	else:
		form = loginForm()
	return render(request, 'login.html', {'form' : form})
