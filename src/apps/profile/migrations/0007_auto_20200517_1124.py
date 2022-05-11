# Generated by Django 3.0.6 on 2020-05-17 02:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0006_auto_20200515_0701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.EmailValidator()], verbose_name='Дополнительный адрес электронной почты'),
        ),
    ]
