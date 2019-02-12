from django.shortcuts import render,redirect
from django.contrib.auth import logout as djangoLogout

# Create your views here.
def logout(request):
	'''
	Backend to perform logout.
	'''
	djangoLogout(request)
	return redirect('/login')
