from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    if request.method == 'POST':
        return render(request, 'capstone_project/index.html', {'POST': 'this is post method'})
    else:
        return render(request, 'capstone_project/index.html', {'GET': 'this is get method'})