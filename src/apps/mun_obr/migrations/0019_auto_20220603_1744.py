# Generated by Django 3.0.14 on 2022-06-03 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mun_obr', '0018_mun_obr_news_create_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statement',
            name='file',
        ),
        migrations.AlterField(
            model_name='statement',
            name='tab_1_file_1',
            field=models.FileField(blank=True, upload_to='mun_obr_files', verbose_name='Файл 1'),
        ),
    ]