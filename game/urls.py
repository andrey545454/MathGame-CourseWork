from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('games/', views.games, name='games'),
    path('games/<int:pk>', views.answer_game, name='answer_game'),

    # path('games/<int:pk>/reg', views.reg_to_game, name='reg_to_game'),

    # path('teams/', views.teams, name='teams'),
    # path('create_team/', views.create_team, name='create_team'),
    # path('delete_team/<int:pk>/', views.del_team, name='del_team'),
    # path('selected_team/<int:pk>/', views.selected_team, name='selected_team'),
    # path('add_to_team/<int:pk>/', views.add_player, name='add_player'),
    # path('leave_team/<int:pk>/', views.leave_team, name='leave_team'),
    # path('remove_player/<int:pk_team>/<int:pk_player>/', views.del_player, name='del_player'),

    # path('invites/', views.invites, name='invites'),

    path('profile/', views.profile, name='profile'),

    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),

    path('results/', views.results, name='results'),
    path('results/<int:pk>', views.results_game, name='results_game'),

    # path('get_teams_with_captain/', views.get_teams_with_captain, name='get_teams_with_captain'),
    # path('get_players_in_team/<int:pk>/', views.get_players_in_team, name='get_players_in_team'),
]