from django.shortcuts import render

# Create your views here.
def docs(request):
        return render(request, 'docs.html')
