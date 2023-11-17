from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE

from .models import Player, Announcement, Response


class PlayerForm(forms.ModelForm):
    role = forms.CharField(label=_('Класс персонажа'))

    class Meta:
        model = Player
        fields = ['role',]


class CodeForm(forms.Form):
    code = forms.CharField(label=_("Код подтверждения"), max_length=6)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(CodeForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        input_code = cleaned_data.get('code')
        player = Player.objects.get(user= self.request.user)
        if input_code != player.auth_code:
            raise ValidationError(
                {'code': 'Код введен неверно. Введите код, который поступил вам в письме после регистрации'}
            )
        return cleaned_data


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label=_('Эл.почта'))
    username = forms.CharField(label=_('Имя пользователя'))
    role = forms.ChoiceField(
        choices=Player.ROLES,
        label=_('Игровой класс'),
    )

    def save(self, commit=True):
        user = super().save()
        users_group = Group.objects.get(name='Users')
        user.groups.add(users_group)
        return user

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']


class AnnouncementForm(forms.ModelForm):
    header = forms.CharField(label=_('Заголовок'))

    class Meta:
        model = Announcement
        fields = ['header', 'body',]
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}


class ResponseForm(forms.ModelForm):
    text = forms.TextInput()

    class Meta:
        model = Response
        fields = ['text']