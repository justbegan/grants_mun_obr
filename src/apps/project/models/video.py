from django.db import models
from .project import Project


class Video(models.Model):
    url = models.TextField("Url", max_length=1000)
    description = models.TextField("Описание", max_length=1000)