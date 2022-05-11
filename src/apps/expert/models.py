from django.db import models
from django.contrib.auth.models import User
from django.apps import apps


class ExpertManager(models.Manager):
    def get_queryset(self):
        return super(ExpertManager, self).get_queryset().filter(groups__name='expert')


class Expert(User):
    EXPERT_GROUP = 'expert'
    objects = ExpertManager()

    def full_name(self):
        return self.last_name + ' ' + self.first_name

    class Meta:
        proxy = True
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'

    def __str__(self):
        count = 0
        str_count = ''
        if hasattr(self, 'contest'):
            projects = apps.get_model('project', 'Project').objects.filter(experts__id=self.id,
                                                                           contest=self.contest).all()
            count = len(projects)
            str_count = " (Кол-во назначенных проектов: %d)" % (count)
        return self.last_name + ' ' + self.first_name + ' ' + self.profile.middle_name + str_count


class Applicant(User):

    class Meta:
        proxy = True
        verbose_name = 'Заявитель'
        verbose_name_plural = 'Заявители'


