from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import json

from .forms import *
from .models import *

# Create your views here.


def index(request):
    return render(request, 'index.html')


def register(request):
    """
    Регистрация нового игрока в системе
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Player.objects.create(
                user=user,
                status=PlayerStatus.objects.get_or_create(name='Активный')
            ).save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'registration/registration.html', {'form': form})


def games(request):
    """
    Страница с доступными играми
    """
    now = timezone.now()
    g = Game.objects.filter(end_time__gte=now)
    started_g = g.filter(start_time__lt=now)
    not_started_g = g.filter(start_time__gte=now)

    return render(request, 'game/games.html',
                  {'not_started_games': not_started_g,
                   'started_games': started_g})


@login_required
def reg_to_game(request, pk):
    """
    Страница с регистрацией на выбранную игру
    """
    # try:
    #     g = Game.objects.get(pk=pk)
    #     cur_player = Player.objects.get(user=request.user)
    #
    #     if request.method == 'POST':
    #         form = RegToGameForm(request.POST, initial={'game': g})
    #
    #         if form.is_valid():
    #             if cur_player in form.cleaned_data['players']:
    #                 participation = form.save()
    #                 return redirect('/')
    #             form.add_error('team', 'Вы должны быть капитаном той команды, которую выбрали!')
    #     else:
    #         form = RegToGameForm(initial={'game': g})
    #
    #     return render(request, 'game/reg_to_game.html', {'form': form})
    #
    # except Game.DoesNotExist:
    #     return redirect('/')


# @login_required
# def teams(request):
#     """
#     Страница с командами
#     """
#     teams = Team.objects.filter(players__user=request.user, status__name='Активный')
#     return render(request, 'team/teams.html', {'teams': teams})


# @login_required
# def create_team(request):
#     """
#     Страница для создания новой команды
#     """
#
#     init_player = Player.objects.get(user=request.user)
#     init_status = TeamStatus.objects.get(name='Активный')
#
#     init_data = {
#         'captain': init_player,
#         'status': init_status
#     }
#
#     if request.method == 'POST':
#         form = CreateTeamForm(request.POST, initial=init_data)
#         if form.is_valid():
#             team = form.save()
#             team.players.add(init_player)
#             return redirect('/')
#     else:
#         form = CreateTeamForm(initial=init_data)
#
#     return render(request, 'team/create_team.html', {'form': form})


# @login_required
# def del_team(request, pk):
#     """
#     Страница для удаления команды (отметка неактивный)
#     """
#
#     try:
#         team = Team.objects.get(pk=pk, status__name='Активный')
#         captain = team.captain
#         players = team.players.all()
#
#         cur_player = players.get(user=request.user)
#
#         if cur_player == captain:
#             if request.method == 'POST':
#                 team.status = TeamStatus.objects.get(name='Неактивный')
#                 team.save()
#                 return redirect('/')
#
#             return render(request, 'team/delete_team.html', {'name': team.name})
#
#         return redirect('/')
#
#     except Team.DoesNotExist:
#         return redirect('/')


# @login_required
# def selected_team(request, pk):
#     """
#     Страница выбранной команды
#     """
#     try:
#         team = Team.objects.get(pk=pk, status__name='Активный')
#         captain = team.captain
#         players = team.players.all()
#
#         cur_player = players.get(user=request.user)
#
#         return render(request, 'team/selected_team.html',
#                       {'team': team,
#                        'captain': captain,
#                        'players': players,
#                        'cur_player': cur_player,
#                        })
#
#     except Team.DoesNotExist:
#         return redirect('/')


# @login_required
# def add_player(request, pk):
#     """
#     Страница для добавления нового игрока в команду
#     """
#     try:
#         team = Team.objects.get(pk=pk, status__name='Активный')
#         captain = team.captain
#         players = team.players.all()
#
#         cur_player = players.get(user=request.user)
#
#         if captain == cur_player:
#             if request.method == 'POST':
#                 form = AddPlayerForm(request.POST)
#                 if form.is_valid():
#                     user = User.objects.get(username=form.cleaned_data['username'])
#                     new_player = Player.objects.get(user=user)
#                     if new_player not in players:
#                         team.players.add(new_player)
#                         return redirect('/')
#                     else:
#                         form.add_error('username', _('Данный игрок уже в команде'))
#             else:
#                 form = AddPlayerForm()
#
#             return render(request, 'team/add_player.html', {'form': form})
#
#         return redirect('/')
#
#     except Team.DoesNotExist:
#         return redirect('/')


# @login_required
# def del_player(request, pk_team, pk_player):
#     """
#     Страница для удаления игрока из команды
#     """
#
#     try:
#         team = Team.objects.get(pk=pk_team, status__name='Активный')
#         captain = team.captain
#         players = team.players.all()
#         cur_player = players.get(user=request.user)
#
#         try:
#             rem_player = team.players.get(pk=pk_player)
#         except Player.DoesNotExist:
#             return redirect('/')
#
#         if cur_player == captain:
#             if request.method == 'POST':
#                 team.players.remove(rem_player)
#                 return redirect('/')
#
#             return render(request, 'team/del_player.html',
#                           {'name': f'{rem_player.user.first_name} {rem_player.user.last_name}'})
#
#         return redirect('/')
#
#     except Team.DoesNotExist:
#         return redirect('/')


# @login_required
# def leave_team(request, pk):
#     """
#     Страница для выхода из команды
#     """
#
#     invs = Invite.objects.filter(player__user=request.user)
#     teams = invs.filter(team__status__name='Активный')
#     return render(request, 'team/invites.html', {'teams': teams})


# @login_required
# def invites(request):
#     """
#     Страница для обработки приглашений в команду
#     """
#
#     invs = Invite.objects.filter(player__user=request.user)
#     teams = invs.filter(team__status__name='Активный')
#     return render(request, 'team/invites.html', {'teams': teams})


@login_required
def profile(request):
    """
    Страница для редактирования информации об игроке
    """
    if request.method == 'POST':
        form = UpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.instance)
            return redirect('/')
    else:
        form = UpdateForm(instance=request.user)
    return render(request, 'profile.html', {'form': form, 'user': request.user})


# @login_required
# def get_teams_with_captain(request):
#     cur_player = Player.objects.get(user=request.user)
#     data = [{'pk': 0, 'name': '-----'}]+list(Team.objects.filter(captain=cur_player, status__name='Активный').values('pk', 'name'))
#     return JsonResponse(data, safe=False)


# @login_required
# def get_players_in_team(request, pk):
#     try:
#         cur_team = Team.objects.get(pk=pk)
#         data = list(cur_team.players.filter(status__name='Активный').values('pk', 'user__first_name', 'user__last_name'))
#         return JsonResponse(data, safe=False)
#     except Team.DoesNotExist:
#         return JsonResponse({})
