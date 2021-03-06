# Generated by Django 3.0.14 on 2022-03-16 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0008_auto_20200517_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bank_data',
            field=models.CharField(blank=True, max_length=255, verbose_name='Банковские реквизиты '),
        ),
        migrations.AddField(
            model_name='profile',
            name='inn',
            field=models.CharField(blank=True, max_length=255, verbose_name='ИНН организации'),
        ),
        migrations.AddField(
            model_name='profile',
            name='jur_adrs',
            field=models.CharField(blank=True, max_length=255, verbose_name='Юридический адрес'),
        ),
        migrations.AddField(
            model_name='profile',
            name='mail_jur',
            field=models.CharField(blank=True, max_length=255, verbose_name='Адрес электронной почты для направления юридически значимых документов;'),
        ),
        migrations.AddField(
            model_name='profile',
            name='main_fio',
            field=models.CharField(blank=True, max_length=255, verbose_name='ФИО лица, имеющего право подписи без доверенности'),
        ),
        migrations.AddField(
            model_name='profile',
            name='mr_go_name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Наименование МР/ГО'),
        ),
        migrations.AddField(
            model_name='profile',
            name='ogrn',
            field=models.CharField(blank=True, max_length=255, verbose_name='ОГРН организации'),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_2',
            field=models.CharField(blank=True, max_length=255, verbose_name='Контактный телефон'),
        ),
        migrations.AddField(
            model_name='profile',
            name='sec_fio',
            field=models.CharField(blank=True, max_length=255, verbose_name='ФИО ответственного специалиста по взаимодействию с уполномоченным органом'),
        ),
    ]
