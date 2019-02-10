from django.shortcuts import render
from .models import repositories
import os, sys

# Create your views here.
def index(request):
	repos = repositories.objects.values_list().values()
	general = {
		'hostname': 'host.tld',
		'path': '/path/2/storage',
		'space': '2.5TB',
		'lastCheck': 'Nov. 12, 2018',
		'status': 'healthy'
	}
	return render(request, 'information.html', {'repos':repos, 'general':general})
