# Generated by Django 3.0.6 on 2020-05-18 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0016_auto_20200518_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.DecimalField(decimal_places=0, max_digits=2, verbose_name='Оценка'),
        ),
    ]