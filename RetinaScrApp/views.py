from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    index_dict = {'insert_me': "Hello. I am from views.py"}
    return render(request, 'RetinaScrApp/index.html', context=index_dict)
