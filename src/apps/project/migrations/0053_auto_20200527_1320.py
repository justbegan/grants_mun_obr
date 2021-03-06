# Generated by Django 3.0.6 on 2020-05-27 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expert', '0003_applicant'),
        ('project', '0052_auto_20200525_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='project',
            name='experts',
            field=models.ManyToManyField(blank=True, related_name='experts', to='expert.Expert', verbose_name='Эксперты'),
        ),
        migrations.AlterField(
            model_name='project',
            name='request_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата подачи'),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата изменения'),
        ),
    ]
