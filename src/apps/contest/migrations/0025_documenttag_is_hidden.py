# Generated by Django 3.0.6 on 2020-05-22 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0024_auto_20200522_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='documenttag',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name='Скрытый тэг'),
        ),
    ]