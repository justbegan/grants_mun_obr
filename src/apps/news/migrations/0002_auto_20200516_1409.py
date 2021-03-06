# Generated by Django 3.0.6 on 2020-05-16 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='img',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='news/%Y/%m/%d', verbose_name='Картинка'),
        ),
        migrations.AddField(
            model_name='news',
            name='thumb',
            field=models.TextField(default=None, max_length=400, null=True),
        ),
    ]
