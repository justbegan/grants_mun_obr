import uuid

from django.db import models

class Geography(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField("География")
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE, blank=True, null=True
    )

    organization = models.ForeignKey(
        'project.Organization', verbose_name="Организация",
        on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "География"
        verbose_name_plural = "География"