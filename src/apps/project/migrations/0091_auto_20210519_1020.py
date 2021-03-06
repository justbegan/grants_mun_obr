# Generated by Django 3.0.14 on 2021-05-19 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0090_auto_20210507_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericcost',
            name='type',
            field=models.CharField(choices=[('salary', 'Оплата труда штатных работников'), ('payouts', 'Выплаты физическим лицам (за исключением индивидуальных предпринимателей) оказание ими услуг (выполнение работ) по гражданско-правовым договорам'), ('insurance', 'Страховые взносы'), ('office', 'Офисные расходы'), ('travel', 'Командировочные расходы'), ('equipment', 'Приобретение, аренда специализированного оборудования, инвентаря и сопутствующие расходы'), ('devel', 'Разработка и поддержка сайтов, информационных систем и иные аналогичные расходы'), ('legal', 'Оплата юридических, информационных, консультационных услуг и иные аналогичные расходы'), ('events', 'Расходы на проведение мероприятий'), ('publishing', 'Издательские, полиграфические и сопутствующие расходы'), ('other', 'Прочие прямые расходы')], max_length=32, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='full_name',
            field=models.TextField(blank=True, verbose_name='Полное название организации'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='short_name',
            field=models.TextField(blank=True, verbose_name='Сокращенное название организации'),
        ),
    ]
