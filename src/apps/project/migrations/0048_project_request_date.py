# Generated by Django 3.0.6 on 2020-05-19 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0047_auto_20200519_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='request_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
