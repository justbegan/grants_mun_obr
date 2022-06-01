from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.postgres.fields import JSONField, ArrayField
from apps.project.models.education import Education
from django.core.validators import validate_email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    SEX_CHOICES = (
        ('F', 'Женский',),
        ('M', 'Мужской',),
    )

    middle_name = models.CharField("Отчество", max_length=255, blank=True)
    mobile_phone = models.CharField("Мобильный телефон", max_length=20, blank=True)
    birth_date = models.DateField("Дата рождения", null=True, blank=True)
    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES,
        verbose_name='Пол',
        blank=True
    )
    education = models.CharField(
        max_length=32,
        choices=Education.EDU,
        verbose_name='Образование',
        blank=True
    )

    email = models.CharField("Дополнительный адрес электронной почты", max_length=255, blank=True, null=True,
                             validators=[validate_email])
    work_phone = models.CharField("Рабочий телефон", max_length=20, blank=True, null=True)
    phone = models.CharField("Контактный телефон", max_length=20, blank=True, null=True)
    locality = models.CharField("Населенный пункт", max_length=255, blank=True, null=True)
    directions = models.ManyToManyField('contest.Direction', verbose_name="Направления", blank=True)
    organization = models.TextField("Место работы (организация)", blank=True, null=True)
    social = ArrayField(models.CharField("Социальная сеть", max_length=255), blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return 'Профиль ' + self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)

