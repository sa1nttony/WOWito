from django_filters import FilterSet, ModelChoiceFilter, ChoiceFilter
from django.utils.translation import gettext as _

from .models import Player, Announcement, Response, New


class PlayerFilter(FilterSet):
    role = ChoiceFilter(
        choices=Player.ROLES,
        field_name='role',
        label=_('Игровой класс'),
        empty_label=_('Любой'),
    )

    class Meta:
        model = Player
        fields = {
            'user__username': ['icontains'],
            'user__email': ['icontains'],
            'role': ['exact'],
        }


class PlayerDetailFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'announcement__header',
            'announcement__body',
            'announcement__author',
        }


class AnnouncementFilter(FilterSet):
    role = ChoiceFilter(
        choices=Player.ROLES,
        field_name='author__role',
        label=_('Игровой класс'),
        empty_label=_('Любой'),
    )

    class Meta:
        model = Announcement
        fields = {
            'header': ['icontains'],
            'body': ['icontains'],
            'author__user__username': ['exact'],
        }


class NewsFilter(FilterSet):
    class Meta:
        model = New
        fields = {
            'header': ['icontains'],
            'text': ['icontains'],
        }
