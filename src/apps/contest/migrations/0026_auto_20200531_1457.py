# Generated by Django 3.0.6 on 2020-05-31 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0025_documenttag_is_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='status',
            field=models.CharField(choices=[('new', 'Новый'), ('opened', 'Идет прием заявок'), ('check', 'Идет проверка'), ('on_exam', 'Идет независимая экспертиза'), ('closed', 'Прием заявок закрыт')], default='new', max_length=32, verbose_name='Статус'),
        ),
    ]