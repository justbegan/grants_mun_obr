# Generated by Django 3.0.6 on 2020-05-07 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_organization_main_activities'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='members_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='22.  Количество членов (участников) организации: физических лиц, юридических лиц:'),
        ),
    ]