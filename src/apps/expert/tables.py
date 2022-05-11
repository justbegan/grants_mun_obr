import django_tables2 as tables

from apps.contest.models import ScoreSheet
from apps.project.models import Project


class ProjectTable(tables.Table):
    budget_request_sum = tables.Column(verbose_name="Запрашиваемая сумма (руб.)", orderable=False)
    created_on = tables.Column(verbose_name="Дата создания")

    T1 = '''
        {% if record.contest.status == record.contest.ON_EXAM  %}
            <a href="{% url 'user-view-project' record.id %}">{{record.title}}</a>
        {% else %}
            {{record.title}}
        {% endif %}
        '''
    title = tables.TemplateColumn(T1, verbose_name="Название проекта", )

    class Meta:
        model = Project
        fields = ('id', 'title', 'organization__short_name',)
        attrs = {"class": "table table-sm table-responsive"}


class ScoreSheetTable(tables.Table):
    T1 = '''
    <a href="{% url 'user-view-project' record.project_id %}">{{record.project.title}}</a>
    '''
    project__title = tables.TemplateColumn(T1, verbose_name="Проект", orderable=False)

    T_ACTION = '''
    {% if record.status == record.NEW and record.contest.status == record.contest.ON_EXAM%}
        <a href="{% url 'expert-edit-score-sheet' record.project_id %}"><i class="fas fa-pen"></i></a>&nbsp;&nbsp;&nbsp;
        <a onclick="return confirm('Вы уверены?')" href="{% url 'expert-delete-score-sheet' record.id %}"><i class="fas fa-trash"></i></a>
    {% else %}
        <a href="{% url 'expert-view-score-sheet' record.id %}"><i class="fas fa-eye"></i></a>
    {% endif %}
    '''
    action = tables.TemplateColumn(T_ACTION, verbose_name="", orderable=False)

    score_sum = tables.Column(verbose_name="Рейтинг", orderable=False)
    score_total_sum = tables.Column(verbose_name="Рейтинг k", orderable=False)
    class Meta:
        model = ScoreSheet
        fields = ('contest', 'status', 'project__title', 'score_sum', 'score_total_sum', 'created_on')
        attrs = {"class": "table table-sm table-responsive"}
