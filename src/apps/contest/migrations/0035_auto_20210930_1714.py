# Generated by Django 3.0.14 on 2021-09-30 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0034_auto_20210810_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportperiod',
            name='notified',
            field=models.BooleanField(default=False, verbose_name='Уведомленены'),
        ),
        migrations.AlterField(
            model_name='reportperiod',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
    ]