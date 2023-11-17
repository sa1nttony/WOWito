# Generated by Django 4.2.7 on 2023-11-17 14:03

from django.db import migrations, models
import django_lifecycle.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_response_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('sended', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.AlterField(
            model_name='response',
            name='status',
            field=models.CharField(choices=[('NC', 'Не рассмотрено'), ('AG', 'Принят'), ('DC', 'Отклонен')], default='NC', max_length=2),
        ),
    ]