import uuid

from django.db import models


class QuantResult(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField("Название", max_length=600, blank=True)
    count = models.IntegerField("Кол-во")
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Количественный результат"
        verbose_name_plural = "Количественные результаты"