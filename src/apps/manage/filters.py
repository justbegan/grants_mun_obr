import django_filters
from apps.contest.models import ScoreSheet, Contest
from apps.project.models import Report
from apps.project.services import get_open_contest


class ScoreSheetFilter(django_filters.FilterSet):
    contest = django_filters.ModelChoiceFilter(label='Конкурс', empty_label="Все конкурсы", queryset=Contest.objects.all())
    oc = get_open_contest()
    project__direction = django_filters.ModelChoiceFilter(label='Направление', empty_label="Все направления", queryset=oc.directions.all())
    status = django_filters.ChoiceFilter(label='Статус', empty_label="Все статусы", choices=ScoreSheet.STATUS)
    project_id = django_filters.NumberFilter(label='№ проекта', )

    class Meta:
        model = ScoreSheet
        fields = ['project_id', 'author']


class ReportFilter(django_filters.FilterSet):
    project__contest = django_filters.ModelChoiceFilter(label='Конкурсы', empty_label="Все конкурсы",
                                               queryset=Contest.objects.all())
    status = django_filters.ChoiceFilter(label='Статус', empty_label="Все статусы", choices=Report.STATUS)
    project__id = django_filters.NumberFilter(label='№ проекта', )

    class Meta:
        model = Report
        fields = ['project__title', 'project__author']