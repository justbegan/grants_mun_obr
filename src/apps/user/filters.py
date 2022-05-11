import django_filters
from apps.project.models import Project
from apps.contest.models import Direction, Contest
from django.db import models

from apps.project.services import get_open_contest


class ProjectFilter(django_filters.FilterSet):
    contest = django_filters.ModelChoiceFilter(label='Конкурсы', empty_label="Все конкурсы", queryset=Contest.objects.all())
    oc = get_open_contest()
    direction = django_filters.ModelChoiceFilter(label='Направление', empty_label="Все направления", queryset=oc.directions.all())
    status = django_filters.ChoiceFilter(label='Статус', empty_label="Все статусы", choices=Project.STATUS)
    id = django_filters.NumberFilter(label='№ проекта')
    inn = django_filters.CharFilter(label='ИНН', field_name='organization__inn')  # , lookup_expr='contains'

    class Meta:
        model = Project
       
        exclude = ['request_file']