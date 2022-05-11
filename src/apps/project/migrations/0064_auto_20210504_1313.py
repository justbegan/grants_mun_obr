# Generated by Django 3.0.14 on 2021-05-04 04:13
import uuid

from django.db import migrations

def gen_uuid(apps, schema_editor):
    Goal = apps.get_model('project', 'Goal')
    for row in Goal.objects.all():
        row.guid = uuid.uuid4()
        row.save(update_fields=['guid'])

class Migration(migrations.Migration):

    dependencies = [
        ('project', '0063_goal_guid'),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
