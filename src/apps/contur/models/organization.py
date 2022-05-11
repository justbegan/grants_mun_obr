import datetime
from django.contrib.postgres.fields import JSONField
from django.core.validators import validate_email
from django.db import models


class Organization(models.Model):
    ogrn = models.CharField("ОГРН", max_length=255, blank=False, unique=True)
    inn = models.CharField("ИНН", max_length=255, blank=True, unique=True)
    
    full_name = models.CharField("Полное название организации", max_length=2048, blank=True)
    short_name = models.CharField("Сокращенное название организации", max_length=2048, blank=True)

    updated_on = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    created_on = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    request_ver = models.CharField("Версия запроса", blank=True, max_length=100 )
    
    # Базовые реквизиты
    basic  = JSONField(default={},null=False)
    # Расширенная аналитика
    analytics  = JSONField(default={},null=False)
    # Расширенные сведения на основе ЕГРЮЛ/ЕГРИП
    egr_details  = JSONField(default={},null=False)

    # Выписка из ЕГРЮЛ/ЕГРИП
    file_egr = models.FileField(upload_to='contur/%s' % datetime.date.today().year, verbose_name="Файл", null=True, blank=True)
    


    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"
        ordering = ['inn']
