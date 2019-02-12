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
<<<<<<< HEAD
			print(form.fields['name'])
			print(form.fields['password'])
			return redirect('http://duckduckgo.com')
			if authenticate(username=form['name'], password=form['password']) is not None:
=======
			if authenticate(username=form['name'].value(), password=form['password'].value()) is not None:
>>>>>>> c7067e0896cb6f661ab9a6cdb1e5f6f227879ab9
				return redirect('http://zoerb.cc:8080/')
		return redirect('http://duckduckgo.com/{}'.format(form['name'].value()))
	else:
		form = loginForm()
	return render(request, 'login.html', {'form' : form})
