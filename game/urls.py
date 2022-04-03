from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('games/', views.games, name='games'),
    path('games/<int:pk>/reg', views.reg_to_game, name='reg_to_game'),

    path('teams/', views.teams, name='teams'),
    path('teams/create', views.create_team, name='create_team'),
    path('teams/delete/<int:pk>', views.del_team, name='del_team'),
    path('teams/<int:pk>', views.selected_team, name='selected_team'),
    path('teams/<int:pk>/add', views.add_player, name='add_player'),
    path('teams/<int:pk>/leave', views.leave_team, name='leave_team'),
    path('teams/<int:pk_team>/del/<int:pk_player>', views.del_player, name='del_player'),

    path('invites/', views.invites, name='invites'),

    path('profile/', views.profile, name='profile'),

    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),

    path('get_teams_with_captain/', views.get_teams_with_captain, name='get_teams_with_captain'),
    path('get_players_in_team/<int:pk>', views.get_players_in_team, name='get_players_in_team'),
]