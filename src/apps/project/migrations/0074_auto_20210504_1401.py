# Generated by Django 3.0.14 on 2021-05-04 05:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0073_auto_20210504_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
