import random

from django.db import models
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django_lifecycle import LifecycleModel, hook, AFTER_CREATE, AFTER_UPDATE
from django.urls import reverse
from django.template.loader import render_to_string
from tinymce.models import HTMLField

from WOWito.settings import *
# Create your models here.


class Player(LifecycleModel):
    tank = 'TK'
    heal = 'HL'
    damagedealer = 'DD'
    trader = 'TD'
    guildmaster = "GM"
    questgiver = 'QG'
    blacksmith = 'BM'
    tanner = 'TN'
    potionmaker = 'PM'
    spellmaster = 'SM'
    ROLES = [
        (tank, 'Танк'),
        (heal, 'Лекарь'),
        (damagedealer, 'Боец'),
        (trader, 'Торговец'),
        (guildmaster, 'Мастер гильдии'),
        (questgiver, 'Квестодатель'),
        (blacksmith, 'Кузнец'),
        (tanner, 'Кожевник'),
        (potionmaker, 'Зельевар'),
        (spellmaster, 'Мастер заклинаний')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLES, default=damagedealer)
    confirmed = models.BooleanField(default=False)
    auth_code = models.CharField(max_length=6, null=True)

    def confirm(self):
        self.confirmed = True
        self.save()

    @hook(AFTER_CREATE)
    def send_code(self):
        code = ''
        for i in range(6):
            i = random.randint(0, 9)
            code += str(i)
        self.auth_code = code
        self.save()

        html_content = render_to_string(
            'confirm_code.html',
            {
                'user': self.user.username,
                'code': self.auth_code
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Здравствуйте, {self.user.username}',
            body='',
            from_email=None,
            to=[self.user.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


class Announcement(LifecycleModel):
    header = models.CharField(max_length=256)
    body = HTMLField()
    author = models.ForeignKey(Player, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('announcements_detail', args=[str(self.id)])


class Response(LifecycleModel):
    not_considered = 'NC'
    agreed = 'AG'
    declined = 'DC'
    STATUSES = [
        (not_considered, 'Не рассмотрено'),
        (agreed, 'Принят'),
        (declined, 'Отклонен')
    ]

    author = models.ForeignKey(Player, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=2, choices=STATUSES, default='NC')

    def get_success_url(self):
        return reverse('announcements_detail', args=[str(self.announcement.id)])

    @hook(AFTER_CREATE)
    def response_added(self):
        html_content = render_to_string(
            template_name='response_added.html',
            context={
                'author': self.author.user.username,
                'announcement_author': self.announcement.author.user.username,
                'header': self.announcement.header,
                'text': self.text,
                'redirect_url': f'{SITE_URL}/announcements/{self.announcement.id}',
            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Отклик на ваше объявление {self.announcement.header}',
            body='',
            from_email=None,
            to=[self.announcement.author.user.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @hook(AFTER_UPDATE)
    def status_changed(self):
        html_content = render_to_string(
            template_name='status_changed.html',
            context={
                'announcement_owner': self.announcement.author.user.username,
                'status': self.status,
                'user': self.author.user.username,
                'announcement_header': self.announcement.header,
                'redirect_url': f'{SITE_URL}/announcements/{self.announcement.id}',
            },
        )

        msg = EmailMultiAlternatives(
            subject=f'Пользователь рассмотрел ваш отклик на объявление "{self.announcement.header}"',
            body='',
            from_email=None,
            to=[self.author.user.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


class New(LifecycleModel):
    header = models.CharField(max_length=255)
    text = models.TextField()
    sended = models.BooleanField(default=False)