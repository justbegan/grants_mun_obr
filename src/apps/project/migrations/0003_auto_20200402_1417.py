# Generated by Django 3.0.4 on 2020-04-02 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_project_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(blank=True, max_length=3000, verbose_name='Краткое описание проекта (деятельности в рамках проекта)'),
        ),
        migrations.AlterField(
            model_name='project',
            name='finish_date',
            field=models.DateField(blank=True, verbose_name='Дата окончания реализации проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='further_progress',
            field=models.TextField(blank=True, max_length=2500, verbose_name='Дальнейшее развитие проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='geography',
            field=models.TextField(blank=True, max_length=1000, verbose_name='География проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='info_support',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Как будет организовано информационное сопровождение проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='quality_results',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Качественные результаты'),
        ),
        migrations.AlterField(
            model_name='project',
            name='social_significance',
            field=models.TextField(blank=True, max_length=5000, verbose_name='Обоснование социальной значимости проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='sources',
            field=models.TextField(blank=True, max_length=500, verbose_name='Источники ресурсного обеспечения проекта в дальнейшем'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(blank=True, verbose_name='Дата начала реализации проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.TextField(blank=True, max_length=500, verbose_name='Название проекта'),
        ),
    ]
