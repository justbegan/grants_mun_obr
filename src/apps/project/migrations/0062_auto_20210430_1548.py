# Generated by Django 3.0.14 on 2021-04-30 06:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0061_auto_20210430_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
