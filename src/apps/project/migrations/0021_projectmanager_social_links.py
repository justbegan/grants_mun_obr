# Generated by Django 3.0.5 on 2020-05-06 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0020_auto_20200506_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectmanager',
            name='social_links',
            field=models.TextField(blank=True, max_length=600, verbose_name='Ссылка на профиль в социальных сетях'),
        ),
    ]
