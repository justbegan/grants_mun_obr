# Generated by Django 3.0.6 on 2020-05-16 04:35

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0036_auto_20200516_1332'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True, verbose_name='Отчет')),
                ('smeta', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
                ('cost', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('result', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Отчет по проекту',
                'verbose_name_plural': 'Отчеты по проекту',
            },
        ),
    ]
