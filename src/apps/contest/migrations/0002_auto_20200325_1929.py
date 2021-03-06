# Generated by Django 3.0.4 on 2020-03-25 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('opened', 'Идет прием заявок'), ('closed', 'Прием заявок закрыт')], default='new', max_length=32, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='direction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Direction', verbose_name='Направление'),
        ),
    ]
