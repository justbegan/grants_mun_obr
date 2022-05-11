# Generated by Django 3.0.4 on 2020-04-02 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_auto_20200402_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='content',
            field=models.TextField(blank=True, max_length=600, verbose_name='Цель проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('draft', 'Подготовка'), ('new', 'Новый'), ('on_exam', 'На экспертизе'), ('win', 'Выиграл'), ('reject', 'Не выиграл')], default='new', max_length=32, verbose_name='Статус'),
        ),
    ]
