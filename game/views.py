from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RegisterForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})


def index(request):
    return render(request, 'base.html')