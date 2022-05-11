# Generated by Django 3.0.6 on 2020-05-20 01:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0049_auto_20200519_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='report',
            name='request_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='report',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]