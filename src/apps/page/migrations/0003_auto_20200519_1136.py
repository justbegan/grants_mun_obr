# Generated by Django 3.0.6 on 2020-05-19 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0017_auto_20200518_2158'),
        ('page', '0002_page_show_documents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='show_documents',
        ),
        migrations.AddField(
            model_name='page',
            name='related_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='contest.DocumentTag', verbose_name='Связанный тэг документов'),
        ),
    ]
