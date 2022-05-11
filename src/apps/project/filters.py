import django_filters

from apps.contest.models import Direction, Contest
from .models import Project, Regions


class RegionFilter(django_filters.ChoiceFilter):

    def __init__(self, *args, **kwargs):
        super(django_filters.ChoiceFilter, self).__init__(*args, **kwargs)
        self.extra['choices'] = [(region, region) for region in Regions.get_region_names()]
        self.extra['empty_label'] = "Все районы"

    def filter(self, qs, region_name):
        values = []
        if region_name:
            values = Regions.get_by_region(region_name)

        return super(django_filters.ChoiceFilter, self).filter(qs, values)


class ProjectFilter(django_filters.FilterSet):
    STATUS = (
        (Project.ON_EXAM, 'На экспертизе'),
        (Project.WIN, 'Проект, получивший поддержку'),
        (Project.NOT_WIN, 'Проект, не получивший поддержку'),
        (Project.REJECT, 'Отклонена'),
    )
    organization__inn = django_filters.CharFilter(label="", lookup_expr='iexact')
    organization__ogrn = django_filters.CharFilter(label="", lookup_expr='iexact')
    organization__short_name = django_filters.CharFilter(label="", lookup_expr='icontains')
    organization__geography__name = RegionFilter(label="", lookup_expr='in')
    title = django_filters.CharFilter(label="", lookup_expr='icontains')
    id = django_filters.CharFilter(label="", lookup_expr='iexact')
    direction = django_filters.ModelChoiceFilter(label='', empty_label="Все направления",
                                                 queryset=Direction.objects.all())
    contest = django_filters.ModelChoiceFilter(label='', empty_label="Все конкурсы", queryset=Contest.objects.all())
    status = django_filters.ChoiceFilter(label='', empty_label="Все статусы", choices=STATUS)

    class Meta:
        model = Project

        exclude = ['request_file']
