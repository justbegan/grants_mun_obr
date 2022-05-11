# Generated by Django 3.0.6 on 2020-05-17 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0042_auto_20200517_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='num_vote_down',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='num_vote_up',
            field=models.PositiveIntegerField(db_index=True, default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='vote_score',
            field=models.IntegerField(db_index=True, default=0),
        ),
    ]
