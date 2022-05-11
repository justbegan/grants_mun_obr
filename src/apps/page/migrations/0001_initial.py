# Generated by Django 3.0.6 on 2020-05-18 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('html', models.TextField(verbose_name='HTML')),
                ('slug', models.SlugField(max_length=160, unique=True, verbose_name='ЧПУ')),
            ],
            options={
                'verbose_name': 'Страница',
                'verbose_name_plural': 'Страницы',
                'ordering': ['title'],
            },
        ),
    ]
