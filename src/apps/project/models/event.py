import datetime
import os
import uuid

from django.db import models

from grants import settings


class Event(models.Model):
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        'project.Job', verbose_name="Решаемая задача",
        on_delete=models.CASCADE
    )
    publish_on_found = models.BooleanField(
        "Целесообразно ли размещение сведений о мероприятии на информационных ресурсах фонда?")
    name = models.TextField(
        "Мероприятие, его содержание, место проведения")
    start_date = models.DateField("Дата начала")
    finish_date = models.DateField("Дата окончания")
    result = models.TextField(
        "Ожидаемые результаты")

    """отчет заполняетсяу выигравших проектов"""
    report = models.TextField("Отчет", null=True, blank=True)

    class Meta:
        ordering = ['pk']


''' Файлы отчетов '''
class EventFile(models.Model):
    event = models.ForeignKey(
        Event, verbose_name="Мероприятие",
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to='projects/reports/%s' % datetime.date.today().year, verbose_name="Файл")

    def delete(self, *args, **kwargs):
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        except Exception:
            pass
        super(EventFile, self).delete(*args, **kwargs)
