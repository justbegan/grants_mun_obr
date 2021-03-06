# Generated by Django 3.0.14 on 2022-05-17 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mun_obr', '0010_auto_20220513_2126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messeges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
                ('messege', models.CharField(blank=True, max_length=255)),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
                ('statement_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='statement_chat', to='mun_obr.Statement')),
            ],
        ),
    ]
