from django import template
from django.utils.translation import gettext as _


register = template.Library()

@register.filter()
def roles_translator(role):
    ROLES = [
        ('TK', _('Танк')),
        ('HL', _('Лекарь')),
        ('DD', _('Боец')),
        ('TD', _('Торговец')),
        ("GM", _('Мастер гильдии')),
        ('QG', _('Квестодатель')),
        ('BM', _('Кузнец')),
        ('TN', _('Кожевник')),
        ('PM', _('Зельевар')),
        ('SM', _('Мастер заклинаний')),
    ]
    for r in ROLES:
        if role == r[0]:
            translated_role = r[1]

    return translated_role


@register.filter()
def status_translator(status):
    STATUSES = [
        ('NC', _('Не рассмотрено')),
        ('AG', _('Принято')),
        ('DC', _('Отклонено'))
    ]
    for s in STATUSES:
        if status == s[0]:
            translated_status = s[1]

    return translated_status