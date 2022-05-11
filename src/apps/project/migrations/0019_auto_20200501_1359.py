# Generated by Django 3.0.5 on 2020-05-01 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0018_auto_20200501_0913'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='geography',
        ),
        migrations.CreateModel(
            name='Geography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='География')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Organization', verbose_name='Организация')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'География',
                'verbose_name_plural': 'География',
            },
        ),
    ]
