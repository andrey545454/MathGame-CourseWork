from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import *


class RegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя
    """

    first_name = forms.CharField(label=_('Имя'))
    last_name = forms.CharField(label=_('Фамилия'))
    username = forms.CharField(label=_('Логин'))
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']


class UpdateForm(UserChangeForm):
    """
    Форма для обновления пользователя
    """

    first_name = forms.CharField(label=_('Имя'))
    last_name = forms.CharField(label=_('Фамилия'))
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CreateTeamForm(forms.ModelForm):
    """
    Форма для создания команды
    """

    name = forms.CharField(label=_('Название команды'))

    class Meta:
        model = Team
        fields = ['name', 'captain', 'status']
        widgets = {
            'captain': forms.HiddenInput(),
            'status': forms.HiddenInput()
        }


class AddPlayerForm(forms.Form):
    """
    Форма добавления пользователя в команду
    """

    username = forms.CharField(label=_('Логин игрока'))

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            User.objects.get(username=data)
        except User.DoesNotExist:
            raise ValidationError(_('Данный игрок не зарегистрирован в системе'))

        return data


class RegToGameForm(forms.ModelForm):
    """
    Форма регистрации команды в игру
    """

    team = forms.ChoiceField(label=_('Команда'), widget=forms.Select(attrs={'id': 'team'}))
    players = forms.MultipleChoiceField(label=_('Игроки'), widget=forms.SelectMultiple(attrs={'id': 'users'}))

    class Meta:
        model = Participation
        fields = ['game', 'team', 'players']
        widgets = {
            'game': forms.HiddenInput(),
        }
