import uuid

from django.db import models

class Job(models.Model):
    content = models.TextField("Задача проекта", max_length=300)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )


    class Meta:
        ordering = ['content']