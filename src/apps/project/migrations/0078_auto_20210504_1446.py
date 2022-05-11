# Generated by Django 3.0.14 on 2021-05-04 05:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0077_auto_20210504_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericcost',
            name='guid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.DeleteModel(
            name='Insurance',
        ),
    ]