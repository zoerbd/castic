from django.shortcuts import render, redirect
from django.conf import settings
from .forms import integrateInformation
import os, sys, json, subprocess

# Create your views here.
def integrate(request):
	'''
	Backend for ansible based automated integration
	'''
	if request.method == 'POST':
		form = integrateInformation(request.POST)
		if form.is_valid():
			__renderAnsible__(form['user'].value(), form['password'].value(), form['dest'].value())
		return redirect('/')
	return render(request, 'integrate.html', {"form": integrateInformation()})


def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        return subprocess.check_output(command, shell=True).decode('utf-8')

def __renderAnsible__(user, pw, dest):
		'''
		This function renders the ansible configuration and roles 
		and executes it on after that on remote machine.
		Integration is based on my shell script to integrate restic.
		'''
		return
