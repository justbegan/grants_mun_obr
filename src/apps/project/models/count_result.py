from django.db import models

class CountCategroy(models.Model):
    title = models.CharField("Количественные категории", max_length=255)

class CountResult(models.Model):
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )
    count_category = models.ForeignKey(
        CountCategroy, verbose_name="Категория",
        on_delete=models.CASCADE
    )