# Generated by Django 3.0.6 on 2020-05-19 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0019_auto_20200519_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='direction',
            name='max_sum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Максимальная сумма бюджета гранта'),
        ),
    ]