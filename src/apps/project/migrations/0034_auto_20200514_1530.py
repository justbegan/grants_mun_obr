# Generated by Django 3.0.6 on 2020-05-14 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0033_auto_20200514_1340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-created_on'], 'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
    ]
