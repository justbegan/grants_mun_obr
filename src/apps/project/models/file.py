import datetime

from django.db import models
from .project import Project
from django.conf import settings
import os


class ProjectFile(models.Model):
    TYPE_LETTER = 'letter'
    TYPE_PRESENTATION = 'presentation'
    
    TYPE_MANAGER = 'manager'
    TYPE_MANAGER_PHOTO = 'manager_photo'

    TYPE_ORGANIZATION_EGRUL = 'organization_egrul'
    TYPE_ORGANIZATION_USTAV = 'organization_ustav'
    TYPE_ORGANIZATION_MINUST = 'organization_minust'
    TYPE_ORGANIZATION_NALOG = 'organization_nalog'
    TYPE_ORGANIZATION_SOGR = 'organization_sogr'
    TYPE_ORGANIZATION_ETC = 'organization_etc'
    TYPE_PROJECT_REQUEST = 'project_request'
    
    TYPE = (
        (TYPE_LETTER, 'Письма поддержки'),
        (TYPE_PRESENTATION, 'Описание проекта'),
        (TYPE_MANAGER, 'Дополнительные документы об организации'),
        (TYPE_MANAGER_PHOTO, 'Фотография руководителя проекта'),
        (TYPE_ORGANIZATION_EGRUL, 'Файл сведений из ЕГРЮЛ (выписка)'),
        (TYPE_ORGANIZATION_USTAV, 'Файл устава'),
        (TYPE_ORGANIZATION_MINUST, 'Копия справки с Минюста'),
        (TYPE_ORGANIZATION_NALOG, 'Копия справки с налоговой об отсутствии задолженности'),
        (TYPE_ORGANIZATION_SOGR, 'Копия свидетельства о государственной регистрации'),
        (TYPE_ORGANIZATION_ETC, 'Дополнительные документы об организации (при наличии) файлы'),
        (TYPE_PROJECT_REQUEST, 'Отсканированная копия заявления'),
    )

    type = models.CharField(
        max_length=32,
        choices=TYPE,
        verbose_name='Тип'
    )

    project = models.ForeignKey(
        Project, verbose_name="Проект",
        on_delete=models.CASCADE
    )
    file = models.FileField(upload_to='projects/%s' % datetime.date.today().year, verbose_name="Файл")

    def delete(self, *args, **kwargs):
        try:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        except Exception:
            pass
        super(ProjectFile, self).delete(*args,**kwargs)
