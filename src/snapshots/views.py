from django.shortcuts import render, redirect
from castic.globals import loginRequired

# Create your views here.
@loginRequired
def snapshots(request):
	return redirect('/')