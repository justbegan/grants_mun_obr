# Generated by Django 3.0.14 on 2021-05-07 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0089_auto_20210504_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='position',
            field=models.TextField(blank=True, max_length=600, verbose_name='Должность руководителя проекта в организации-заявителе'),
        ),
    ]
