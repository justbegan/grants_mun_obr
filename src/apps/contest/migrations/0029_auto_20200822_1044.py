# Generated by Django 3.0.6 on 2020-08-22 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0028_auto_20200804_0847'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='score',
            options={'ordering': ['criteria__title'], 'verbose_name': 'Оценка', 'verbose_name_plural': 'Оценки'},
        ),
        migrations.AlterField(
            model_name='score',
            name='updated_on',
            field=models.DateTimeField(),
        ),
    ]
