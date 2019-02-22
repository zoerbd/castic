from django.shortcuts import render
from castic.globals import loginRequired

# Create your views here.
@loginRequired
def docs(request):
        return render(request, 'docs.html')
