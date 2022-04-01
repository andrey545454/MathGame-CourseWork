from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm
from .models import *

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
    g = Game.objects.all()
    return render(request, 'games.html', {'games': g})


@login_required
def selected_game(request, pk):
    g = Game.objects.all()
    print(pk)
    return render(request, 'games.html', {'games': g})


@login_required
def teams(request):
    teams = Team.objects.filter(players__user=request.user)
    return render(request, 'teams.html', {'teams': teams})


@login_required
def profile(request):
    return render(request, 'profile.html')