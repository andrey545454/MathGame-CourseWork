from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
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


# class CreateTeamForm(forms.ModelForm):
#     """
#     Форма для создания команды
#     """
#
#     name = forms.CharField(label=_('Название команды'))
#
#     class Meta:
#         model = Team
#         fields = ['name', 'captain', 'status']
#         widgets = {
#             'captain': forms.HiddenInput(),
#             'status': forms.HiddenInput()
#         }


# class AddPlayerForm(forms.Form):
#     """
#     Форма добавления пользователя в команду
#     """
#
#     username = forms.CharField(label=_('Логин игрока'))
#
#     def clean_username(self):
#         data = self.cleaned_data['username']
#         try:
#             User.objects.get(username=data)
#         except User.DoesNotExist:
#             raise ValidationError(_('Данный игрок не зарегистрирован в системе'))
#
#         return data


# class RegToGameForm(forms.ModelForm):
#     """
#     Форма регистрации команды в игру
#     """
#
#     team = forms.ChoiceField(label=_('Команда'), widget=forms.Select(attrs={'id': 'team'}))
#     players = forms.MultipleChoiceField(label=_('Игроки'), widget=forms.SelectMultiple(attrs={'id': 'users'}))
#
#     class Meta:
#         model = Participation
#         fields = ['game', 'team', 'players']
#         widgets = {
#             'game': forms.HiddenInput(),
#         }


class AnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.game = kwargs.pop('game')
        self.player = kwargs.pop('player')
        self.problems = kwargs.pop('problems')
        super().__init__(*args, **kwargs)

        for i, problem in enumerate(self.problems):

            try:
                ans = Answer.objects.get(
                    game=self.game,
                    player=self.player,
                    problem=problem,
                )

                self.fields[f'answer_{i}'] = forms.CharField(
                    required=False,
                    label=_(f'Ответ на задачу {i + 1}'),
                    max_length=100,
                    initial=ans.answer
                )

            except Answer.DoesNotExist:
                self.fields[f'answer_{i}'] = forms.CharField(
                    required=False,
                    label=_(f'Ответ на задачу {i+1}'),
                    max_length=100
                )

    def save(self):
        for i in range(len(self.problems)):
            obj, created = Answer.objects.update_or_create(
                game=self.game,
                player=self.player,
                problem=self.problems[i],
                defaults={
                    'answer': self.cleaned_data[f'answer_{i}']
                }
            )
