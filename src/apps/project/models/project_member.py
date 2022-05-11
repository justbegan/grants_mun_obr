import uuid

from django.db import models
from .education import Education


class ProjectMember(models.Model):
    education = models.CharField(
        max_length=32,
        choices=Education.EDU,
        verbose_name='Оразование',
        blank=True
    )
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )
    position = models.TextField(
        "Должность руководителя проекта в организации-заявителе", max_length=600, blank=True)
    last_name = models.CharField("Фамилия", max_length=255, blank=True)
    first_name = models.CharField("Имя", max_length=255, blank=True)
    middle_name = models.CharField("Отчество", max_length=255, blank=True)
    info = models.TextField("Дополнительные сведения",
                            max_length=600, blank=True)

    def works(self):
        return self.institution_set.all().filter(type='work')

    def educations(self):
        return self.institution_set.all().filter(type='education')

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.middle_name

    class Meta:
        ordering = ['id']


class ProjectMemberOrgaziation(models.Model):
    EDU = 'edu'
    WORK = 'work'

    TYPE = (
        (EDU, 'Образовательные организации и специальности'),
        (WORK, 'Место работы'),
    )
    type = models.CharField(
        max_length=32,
        choices=TYPE,
        verbose_name='Тип'
    )
    manager = models.ForeignKey(
        'project.ProjectManager', verbose_name="Менеджер проекта",
        on_delete=models.CASCADE, null=True, blank=True
    )

    member = models.ForeignKey(
        ProjectMember, verbose_name="Участник проекта",
        on_delete=models.CASCADE, null=True, blank=True
    )
    position = models.CharField(
        "Должность/Специальность", max_length=255, blank=True)
    organization = models.CharField("Организация", max_length=255, blank=True)
    start_date = models.DateField("Год начала", null=True, blank=True)
    finish_date = models.DateField("Год окончания", null=True, blank=True)
