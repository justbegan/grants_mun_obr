# Generated by Django 3.0.14 on 2021-05-04 04:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0065_auto_20210504_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='targetgroup',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
