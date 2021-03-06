# Generated by Django 3.0.6 on 2020-05-14 03:46

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0004_auto_20200514_1102'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='social',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, verbose_name='Социальная сеть'), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='profile',
            name='education',
            field=models.CharField(blank=True, choices=[('srednee_obshee', 'Среднее общее'), ('srednee_proff', 'Среднее профессиональное'), ('nezakonchennoe_vusshee', 'Не законченное высшее'), ('vusshee', 'Высшее'), ('bolee_odngogo_vishego', 'Более одного высшего'), ('uchenuy', 'Есть ученая степень')], max_length=32, verbose_name='Образование'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Контактный телефон'),
        ),
    ]
