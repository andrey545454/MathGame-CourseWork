from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import json
import itertools

from .forms import *
from .models import *

# Create your views here.


def index(request):
    """
    Главная страница
    """
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
                status=PlayerStatus.objects.get_or_create(name='Активный')[0]
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
    registered_g = set()

    message = None

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        game = not_started_g.get(pk=request.POST['gameId'])
        cur_player = Player.objects.get(user=request.user)

        if 'regBtn' in request.POST:
            try:
                Participation.objects.create(
                    game=game,
                    player=cur_player
                ).save()
                message = _('Поздравляю, вы зарегистрировались на игру')

            except Game.DoesNotExist:
                return redirect('/')

            except IntegrityError:
                return redirect('/')

    if request.user.is_authenticated:
        cur_player = Player.objects.get(user=request.user)
        registered_g = g.filter(participation__player=cur_player)

    return render(request, 'game/games.html',
                  {'not_started_games': not_started_g,
                   'started_games': started_g,
                   'registered_games': registered_g,
                   'message': message})


@login_required
def answer_game(request, pk):
    """
    Страница с формой для определенной игры
    """
    message = None

    try:
        cur_player = Player.objects.get(user=request.user)
        game = Game.objects.get(pk=pk)
        remaining_time = game.end_time-timezone.now()
        Participation.objects.get(game=game, player=cur_player)
        problems = ProblemInGame.objects.filter(game=game).order_by('pos')

        if not problems:
            raise Http404()

        if remaining_time.total_seconds() < 0:
            return redirect('/')

        if request.method == 'POST':
            form = AnswerForm(request.POST, game=game, player=cur_player, problems=problems)
            if form.is_valid():
                form.save()
                message = _('Ваши ответы сохранены! Можете покинуть данную страницу или изменить ответы до конца игры')
        else:
            form = AnswerForm(game=game, player=cur_player, problems=problems)

    except Player.DoesNotExist:
        raise Http404()

    except Game.DoesNotExist:
        raise Http404()

    except Participation.DoesNotExist:
        raise Http404()

    return render(request,
                  'game/answer_game.html',
                  {'game_title': game.name,
                   'probs_and_fields': zip(problems, form),
                   'end_time': game.end_time.isoformat(),
                   'message': message})


# @login_required
# def reg_to_game(request, pk):
#     """
#     Страница с регистрацией на выбранную игру
#     """
#     try:
#         g = Game.objects.get(pk=pk)
#         cur_player = Player.objects.get(user=request.user)
#
#         if request.method == 'POST':
#             form = RegToGameForm(request.POST, initial={'game': g})
#
#             if form.is_valid():
#                 if cur_player in form.cleaned_data['players']:
#                     form.save()
#                     return redirect('/')
#         else:
#             form = RegToGameForm(initial={'game': g})
#
#         return render(request, 'game/reg_to_game.html', {'form': form})
#
#     except Game.DoesNotExist:
#         return redirect('/')


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


def results(request):
    """
    Страница со списком пройденных игр
    """
    now = timezone.now()
    ended_g = Game.objects.filter(end_time__lt=now)

    return render(request, 'game/results.html', {'ended_games': ended_g})


def results_game(request, pk):
    """
    Страница с результатами игроков в данной игре
    """
    players = []

    try:
        game = Game.objects.get(pk=pk)
        answers = Answer.objects.filter(game=game).order_by('problem__pos')

        answers_d = {}
        for answer in answers:
            answers_d[answer.player] = answers_d.get(answer.player, [])+[answer]

        for player in answers_d:

            try:
                score_obj = Score.objects.get(game=game, player=player)
                score = score_obj.score

            except Score.DoesNotExist:
                # Подсчёт очков по формуле
                score = 0
                k = 0
                for i, answer_obj in enumerate(answers_d[player]):
                    correct_answer = answer_obj.problem.problem.answer
                    probably_answer = answer_obj.answer
                    if probably_answer == correct_answer:
                        score += 3+k
                        k += 1
                    else:
                        k = 0

                Score.objects.create(
                    game=game,
                    player=player,
                    score=score
                )

            players.append((player, score))

        players.sort(key=lambda x: x[1], reverse=True)

    except Game.DoesNotExist:
        raise Http404()

    return render(request, 'game/results_game.html', {'players': players})


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
