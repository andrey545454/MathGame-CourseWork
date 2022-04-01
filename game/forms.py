from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
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
    A form that updates a user, with no privileges, from the given username and
    password.
    """

    first_name = forms.CharField(label=_('Имя'))
    last_name = forms.CharField(label=_('Фамилия'))
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

