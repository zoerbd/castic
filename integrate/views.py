from django.shortcuts import render, redirect
from django.conf import settings
import os, sys, json, subprocess

# Create your views here.
def integrate(request):
	'''
	Backend for ansible based automated integration
	'''
	return render(request, 'index.html')


def __shell__(command):
        '''
        This function makes it less pain to get shell answers
        '''
        return subprocess.check_output(command, shell=True).decode('utf-8')
