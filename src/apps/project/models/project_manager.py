from django.core.validators import validate_email
from django.db import models
from .education import Education

class ProjectManager(models.Model):
    education = models.CharField(
        max_length=32,
        choices=Education.EDU,
        verbose_name='Оразование',
        blank=True
    )
    position = models.CharField(
        "Должность руководителя проекта в организации-заявителе", max_length=255, blank=True)
    last_name = models.CharField("Фамилия", max_length=255, blank=True)
    first_name = models.CharField("Имя", max_length=255, blank=True)
    middle_name = models.CharField("Отчество", max_length=255, blank=True)
    degree = models.CharField("Ученая степень", max_length=255, blank=True)
    work_phone = models.CharField("Рабочий телефон", max_length=20, blank=True)
    mobile_phone = models.CharField(
        "Мобильный телефон", max_length=20, blank=True)
    email = models.CharField("Электронная почта", max_length=100, blank=True, validators=[validate_email])
    info = models.TextField("Дополнительные сведения",
                            max_length=600, blank=True)
    photo = models.ImageField(upload_to='projects', verbose_name="Изображение")
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    social_links = models.TextField("Ссылка на профиль в социальных сетях",
                            max_length=600, blank=True)
    academic_rank = models.CharField(
        "Учёное звание, учёная степень руководителя проекта (если имеется):", max_length=255, blank=True)

    def works(self):
        return self.institution_set.all().filter(type='work')

    def work_set(self):
        return self.institution_set.filter(type='work')

    def educations(self):
        return self.institution_set.all().filter(type='education')

    def education_set(self):
        return self.institution_set.filter(type='education')

    def __str__(self):
        return self.last_name + " " + self.first_name + " " + self.middle_name

    class Meta:
        verbose_name = "Менеджер проекта"
        verbose_name_plural = "Менеджеры проекта"