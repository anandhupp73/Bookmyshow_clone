from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'home.html')

def movies(request):
    return render(request,'movie.html')