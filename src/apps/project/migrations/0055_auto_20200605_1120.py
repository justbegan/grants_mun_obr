# Generated by Django 3.0.6 on 2020-06-05 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0054_auto_20200531_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20, verbose_name='Общая сумма расходов организации за предыдущий год'),
        ),
    ]
