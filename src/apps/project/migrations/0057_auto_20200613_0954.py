# Generated by Django 3.0.6 on 2020-06-13 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0056_auto_20200605_1147'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['start_date']},
        ),
        migrations.AlterModelOptions(
            name='institution',
            options={'ordering': ['start_date']},
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('new', 'Подана'), ('on_check', 'На проверке'), ('fix', 'На доработку'), ('on_exam', 'На экспертизе'), ('win', 'Победитель конкурса'), ('not_win', 'Проект, не получивший поддержку'), ('reject', 'Отклонена')], default='draft', max_length=32, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='projectfile',
            name='type',
            field=models.CharField(choices=[('letter', 'Письма поддержки'), ('presentation', 'Описание проекта'), ('manager', 'Дополнительные документы об организации'), ('manager_photo', 'Фотография руководителя проекта'), ('organization_egrul', 'Файл сведений из ЕГРЮЛ (выписка)'), ('organization_ustav', 'Файл устава'), ('organization_minust', 'Копия справки с Минюста'), ('organization_nalog', 'Копия справки с налоговой об отсутствии задолженности'), ('organization_sogr', 'Копия свидетельства о государственной регистрации'), ('organization_etc', 'Дополнительные документы об организации (при наличии) файлы'), ('project_request', 'Отсканированная копия заявления')], max_length=32, verbose_name='Тип'),
        ),
    ]
