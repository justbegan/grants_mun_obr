# Generated by Django 3.0.14 on 2022-05-13 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mun_obr', '0009_statement_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='comment',
            field=models.CharField(blank=True, max_length=250, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='status',
            field=models.CharField(choices=[('На модерации', 'На модерации'), ('На доработке', 'На доработке'), ('Проверка пройдена', 'Проверка пройдена')], default='На модерации', max_length=100, verbose_name='Статус заявки'),
        ),
    ]
