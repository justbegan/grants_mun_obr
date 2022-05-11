import uuid

from django.db import models

class Goal(models.Model):
    content = models.TextField("Цель проекта", max_length=600, blank=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Цель проекта"
        verbose_name_plural = "Цели проекта"