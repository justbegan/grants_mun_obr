# Generated by Django 3.0.5 on 2020-05-06 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0021_projectmanager_social_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectfile',
            name='type',
            field=models.CharField(choices=[('letter', 'Письма поддержки'), ('presentation', 'Описание проекта'), ('manager', 'Дополнительные документы об организации'), ('manger_photo', 'Фотография руководителя проекта'), ('organization_egrul', 'Файл сведений из ЕГРЮЛ (выписка)'), ('organization_ustav', 'Файл устава'), ('organization_minust', 'Копия справки с Минюста'), ('organization_nalog', 'Копия справки с налоговой об отсутствии задолженности'), ('organization_etc', 'Дополнительные документы об организации (при наличии) файлы'), ('project_request', 'Отсканированная копия заявления')], max_length=32, verbose_name='Тип'),
        ),
    ]
