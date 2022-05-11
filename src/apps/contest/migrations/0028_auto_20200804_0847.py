# Generated by Django 3.0.6 on 2020-08-03 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0027_auto_20200716_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('opened', 'Идет прием заявок'), ('check', 'Идет проверка'), ('on_exam', 'Идет независимая экспертиза'), ('closed', 'Конкурс завершен')], default='new', max_length=32, verbose_name='Статус'),
        ),
    ]
