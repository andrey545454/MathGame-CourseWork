from django.http import HttpResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _

from .forms import *
from .models import *

# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Player.objects.create(
                user=user,
                status=PlayerStatus.objects.get(name='Активный')
            ).save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration.html', {'form': form})


def index(request):
    return render(request, 'index.html')


def games(request):
    g = Game.objects.all()
    return render(request, 'game/games.html', {'games': g})


@login_required
def selected_game(request, pk):
    g = Game.objects.all()
    return render(request, 'game/games.html', {'games': g})


@login_required
def teams(request):
    teams = Team.objects.filter(players__user=request.user)
    return render(request, 'team/teams.html', {'teams': teams})


@login_required
def create_team(request):

    init_player = Player.objects.get(user=request.user)
    init_status = TeamStatus.objects.get(name='Активный')

    init_data = {
        'captain': init_player,
        'status': init_status
    }

    if request.method == 'POST':
        form = CreateTeamForm(request.POST, initial=init_data)
        if form.is_valid():
            team = form.save()
            team.players.add(init_player)
            return redirect('/')
    else:
        form = CreateTeamForm(initial=init_data)

    return render(request, 'team/create_team.html', {'form': form})


@login_required
def selected_team(request, pk):
    team = Team.objects.get(pk=pk)
    captain = team.captain
    players = team.players.all()
    cur_player = players.get(user=request.user)

    return render(request, 'team/selected_team.html',
                  {'team': team,
                   'captain': captain,
                   'players': players,
                   'cur_player': cur_player,
                   })


@login_required
def add_player(request, pk):
    team = Team.objects.get(pk=pk)
    captain = team.captain

    players = team.players.all()
    cur_player = players.get(user=request.user)

    if captain == cur_player:
        if request.method == 'POST':
            form = AddPlayerForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username=form.cleaned_data['username'])
                new_player = Player.objects.get(user=user)
                if new_player not in players:
                    team.players.add(new_player)
                    return redirect('/')
                else:
                    form.add_error('username', _('Данный игрок уже в команде'))
        else:
            form = AddPlayerForm()

        return render(request, 'team/add_player.html', {'form': form})

    return redirect('/')


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
    return render(request, 'profile.html', {'form': form, 'user': request.user})
