from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from .forms import RegisterForm

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def games(request):
    return render(request, 'games.html')


def teams(request):
    return render(request, 'teams.html')


def profile(request):
    return render(request, 'profile.html')