import uuid

from django.db import models


class Institution(models.Model):
    EDUCATION = 'education'
    WORK = 'work'

    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    TYPE = (
        (EDUCATION, 'Образовательные учреждения'),
        (WORK, 'Место работы'),
    )
    
    type = models.CharField(
        max_length=32,
        choices=TYPE,
        default=EDUCATION,
        verbose_name='Тип'
    )

    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )

    organization = models.TextField("Организация", max_length=300)
    position = models.CharField("Должность/Специальность", max_length=100)
    
    start_date = models.DateField("Дата начала", null=True)
    finish_date = models.DateField("Дата окончания", null=True)
    in_present = models.BooleanField("По настоящее время", default=False)

    member = models.ForeignKey(
        'project.ProjectMember', verbose_name="Участник проекта",
        on_delete=models.CASCADE, blank=True, null=True
    )
    manager = models.ForeignKey(
        'project.ProjectManager', verbose_name="Руководитель проекта",
        on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ['start_date']
