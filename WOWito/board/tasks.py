from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext as _

from .models import New, Player


@shared_task()
def send_news():
    news_exist = False

    for new in New.objects.all():
        if not new.sended:
            news_exist = True
            break

    if news_exist:
        emails = []
        for email in Player.objects.all().values('user__email'):
            emails.append(email['user__email'])


        html_content = render_to_string(
            template_name='news_notification.html',
            context={
                'news': New.objects.all(),
            }
        )

        msg = EmailMultiAlternatives(
            subject=_('Новости за последнюю неделю'),
            body='',
            from_email=None,
            to=emails
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

        for new in New.objects.all():
            if new.sended == False:
                new.sended = True
                new.save()
