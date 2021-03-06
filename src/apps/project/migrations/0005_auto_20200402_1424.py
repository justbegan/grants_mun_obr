# Generated by Django 3.0.4 on 2020-04-02 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20200325_1929'),
        ('project', '0004_auto_20200402_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='contest',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.Contest', verbose_name='Конкурс'),
        ),
        migrations.AlterField(
            model_name='project',
            name='direction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.Direction', verbose_name='Грантовое направление, которому преимущественно соответствует планируемая деятельность по проекту'),
        ),
        migrations.AlterField(
            model_name='project',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.Subject', verbose_name='Тематика грантового направления, которому преимущественно соответствует планируемая деятельность по проекту'),
        ),
    ]
