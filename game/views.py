from django.http import HttpResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegisterForm, UpdateForm
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
def selected_team(request, pk):
    team = Team.objects.get(pk=pk)
    print(team)
    return render(request, 'teams.html')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)
            return redirect('/')
    else:
        form = UpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})
