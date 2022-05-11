# Generated by Django 3.0.14 on 2021-05-04 06:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0088_auto_20210504_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geography',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
