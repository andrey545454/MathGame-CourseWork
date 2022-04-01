from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.games, name='games'),
    path('games/<int:pk>', views.selected_game, name='selected_game'),
    path('teams/', views.teams, name='teams'),
    path('teams/<int:pk>', views.teams, name='selected_team'),
    path('profile/', views.profile, name='profile'),

    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls'))
]