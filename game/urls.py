from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('games/', views.games, name='games'),
    path('games/<int:pk>', views.selected_game, name='selected_game'),

    path('teams/', views.teams, name='teams'),
    path('teams/create', views.create_team, name='create_team'),
    path('teams/<int:pk>', views.selected_team, name='selected_team'),
    path('teams/<int:pk>/add', views.add_player, name='add_player'),

    path('profile/', views.profile, name='profile'),

    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls'))
]