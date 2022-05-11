from django.db import models
from django.contrib.auth.models import User


class Comment(models.Model):
    TYPE_INTERNAL = 'internal'
    TYPE_EXTERNAL = 'external'

    TYPE = (
        (TYPE_INTERNAL, 'Внутренние'),
        (TYPE_EXTERNAL, 'Общедоступные'),
    )

    type = models.CharField(
        max_length=32,
        choices=TYPE,
        default=TYPE_INTERNAL,
        verbose_name='Тип'
    )
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )
    
    content = models.TextField("Комментарий")
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ['-created_on']
    