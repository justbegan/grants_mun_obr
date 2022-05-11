import django_tables2 as tables
from apps.project.models import Project, Report
from django_tables2.utils import A 


class ProjectTable(tables.Table):
    id = tables.LinkColumn('user-view-project', args=[A('pk')])
    budget_request_sum = tables.Column(verbose_name="Запрашиваемая сумма (руб.)", orderable=False)
    request_date = tables.Column(verbose_name="Дата подачи")
    created_on = tables.Column(verbose_name="Дата создания")

    T1 = '''{% if record.status == record.DRAFT or record.status == record.FIX %}
                <a onclick="return confirm('Вы уверены?')" href="{% url 'user-delete-project' record.id %}">
                    <i class="fas fa-trash"></i>
                </a>
            {% endif %}'''
    delete = tables.TemplateColumn(T1, verbose_name="Удалить", orderable=False)

    T2 = '''{{ record.get_status_display }}'''
    status = tables.TemplateColumn(T2, verbose_name="Статус")
    class Meta:
        model = Project
        fields = ('id', 'status', 'direction', 'title', 'organization__short_name', )
        attrs = {"class": "table table-sm data-table table-responsive"}


class ReportTable(tables.Table):
    id = tables.LinkColumn('user-view-project', args=[A('pk')])

    budget_request_sum = tables.Column(verbose_name="Запрашиваемая сумма (руб.)", orderable=False)
    budget_co_financing_sum = tables.Column(verbose_name="Сумма софинансирования (руб.)", orderable=False)

    T1 = '''
    {% if record.report.status == record.report.DRAFT or record.report.status == record.report.FIX %}
        <a href="{% url 'user-report-project' record.id %}"><i class="fas fa-pen"></i></a>
    {% endif %}
    '''
    edit = tables.TemplateColumn(T1, verbose_name="Изменить", orderable=False)
    class Meta:
        model = Project
        fields = ('id', 'report__status', 'title', 'organization__short_name', )
        attrs = {"class": "table table-sm table-responsive"}