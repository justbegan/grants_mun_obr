# Generated by Django 3.0.6 on 2020-05-15 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0010_auto_20200514_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('opened', 'Идет прием заявок'), ('on_exam', 'Идет независимая экспертиза'), ('closed', 'Прием заявок закрыт')], default='new', max_length=32, verbose_name='Статус'),
        ),
    ]
