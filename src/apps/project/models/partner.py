import uuid

from django.db import models


class Partner(models.Model):
    name = models.CharField("Партнер", max_length=255)
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )
    supports =  models.TextField("Виды поддержки", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Партнер проекта"
        verbose_name_plural = "Партнеры проекта"