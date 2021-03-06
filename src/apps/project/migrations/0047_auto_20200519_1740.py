# Generated by Django 3.0.6 on 2020-05-19 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0046_auto_20200518_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('draft', 'Черновик'), ('new', 'На проверке'), ('fix', 'На доработку'), ('on_exam', 'На экспертизе'), ('win', 'Победитель конкурса'), ('not_win', 'Проект, не получивший поддержку'), ('reject', 'Отклонена')], default='new', max_length=32, verbose_name='Статус'),
        ),
    ]
