import uuid

from django.db import models
from .project import Project


class TargetGroup(models.Model):
    TYPE_PROJECT = 'project'
    TYPE_OGRANIZATION = 'organization'

    TYPE = (
        (TYPE_PROJECT, 'Для проекта'),
        (TYPE_OGRANIZATION, 'Для организации'),
    )

    type = models.CharField(
        max_length=32,
        choices=TYPE,
        default=TYPE_PROJECT,
        verbose_name='Тип'
    )

    title = models.CharField("Название группы", max_length=255)
    project = models.ForeignKey(
        Project, verbose_name="Проект",
        on_delete=models.CASCADE
    )
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    organization = models.ForeignKey(
        'project.Organization', verbose_name="Организация",
        on_delete=models.CASCADE, blank=True, null=True
    )
