from django.shortcuts import redirect
from repositories.models import repositories
from castic.globals import loginRequired

@loginRequired
def clearData(request):
	'''
	This function is the backend for <prot>://<server>/settings/clear_check_data
	It basically does nothing but removes any processed data from index/models 
	(corresponds to table index_repository).
	'''
	repositories.objects.all().delete()
	return redirect('/update/')
