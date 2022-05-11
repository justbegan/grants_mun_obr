import django_tables2 as tables
from apps.project.models import Project, Report
from apps.contest.models import ScoreSheet
from django_tables2.utils import A


class ProjectTable(tables.Table):
    id = tables.LinkColumn('user-view-project', args=[A('pk')], verbose_name="№ Заявки")
    title = tables.LinkColumn('user-view-project', args=[A('pk')], verbose_name="Название проекта")
    budget_request_sum = tables.Column(verbose_name="Запрашиваемая сумма (руб.)", orderable=False)
    # request_date = tables.Column(verbose_name="Дата подачи")
    # updated_on = tables.Column(verbose_name="Изменен")
    averange_score = tables.Column(verbose_name="Средний балл", orderable=False)

    T_EXPERT = '''{% for expert in record.experts.all %}
                    {{ expert.last_name }} {{ expert.first_name }}<br>
                {% endfor %}'''
    experts = tables.TemplateColumn(T_EXPERT, verbose_name="Эксперты", orderable=False)

    T_AUTHOR = '''{{ record.author }} ({{ record.author.last_name }} {{ record.author.first_name }})'''
    author = tables.TemplateColumn(T_AUTHOR, verbose_name="Автор", orderable=False)

    T_DELETE = '''
                <a onclick="return confirm('Вы уверены?')" href="{% url 'user-delete-project' record.id %}">
                    <i class="fas fa-trash"></i>
                </a>
            '''

    # delete = tables.TemplateColumn(T_DELETE, verbose_name="Удалить", orderable=False)

    class Meta:
        model = Project
        fields = ('id', 'status', 'title', 'experts', 'author', 'request_date', 'updated_on', 'averange_score',
                  'budget_request_sum')
        attrs = {"class": "table table-sm table-hover data-table table-responsive"}


class ProjectTableExcel(tables.Table):
    id = tables.LinkColumn('user-view-project', args=[A('pk')], verbose_name="№ Заявки")
    budget_request_sum = tables.Column(verbose_name="Запрашиваемая сумма в руб.", orderable=False)
    budget_co_financing_sum = tables.Column(verbose_name="Сумма софинансирования в руб.", orderable=False)
    #request_date = tables.Column(verbose_name="Дата подачи")
    organization__geography_str = tables.Column(verbose_name="Наименование муниципального района/городского округа", orderable=False)
    status = tables.Column(verbose_name="Итоги первичной проверки (на доработке/допустить/отклонить)", orderable=False)
    checklist_str = tables.Column(verbose_name="Комментарии", orderable=False)

    class Meta:
        model = Project
        fields = ('id',
                  'request_date', 'updated_on',
                  'organization__geography_str', 'organization__ogrn', 'organization__inn', 'organization__legal_address',
                  'title',
                  'direction',
                  'subject',
                  'budget_request_sum',
                  'budget_co_financing_sum',
                  'status',
                  'checklist_str'
                  )


class ScoreSheetTable(tables.Table):
    score_sum = tables.Column(verbose_name="Рейтинг", orderable=False)
    score_total_sum = tables.Column(verbose_name="Рейтинг k", orderable=False)

    T_AUTHOR = '''
                {{record.author}} ({{record.author.last_name}} {{record.author.first_name}})
            '''
    author = tables.TemplateColumn(T_AUTHOR, verbose_name="Автор", orderable=False)

    T_ACTIONS = '''
                <a href="{% url 'expert-view-score-sheet' record.id %}"><i class="fas fa-eye"></i></a>
            '''
    actions = tables.TemplateColumn(T_ACTIONS, verbose_name="", orderable=False)

    updated_on = tables.Column(verbose_name="Обновлен")

    class Meta:
        model = ScoreSheet
        fields = (
            'contest', 'project__title', 'status', 'score_sum', 'score_total_sum', 'author', 'updated_on', 'actions')
        attrs = {"class": "table table-sm table-hover data-table table-responsive"}


class ScoreSheetTableExcel(tables.Table):
    score_sum = tables.Column(verbose_name="Рейтинг", orderable=False)
    score_total_sum = tables.Column(verbose_name="Рейтинг k", orderable=False)

    T_AUTHOR = '''
                    {{record.author}} ({{record.author.last_name}} {{record.author.first_name}})
                '''
    author = tables.TemplateColumn(T_AUTHOR, verbose_name="Автор", orderable=False)

    class Meta:
        model = ScoreSheet
        fields = (
            'project__id', 'project__title', 'status', 'score_sum', 'score_total_sum', 'author', 'updated_on')
        attrs = {"class": "table table-sm table-hover data-table table-responsive"}


class ReportTable(tables.Table):
    project__budget_request_sum = tables.Column(verbose_name="Запрашиваемая сумма", orderable=False)
    project__id = tables.Column(verbose_name="№ Проекта", orderable=False)

    T_AUTHOR = '''
                {{record.project.author}} ({{record.project.author.last_name}} {{record.project.author.first_name}})
            '''
    project__author = tables.TemplateColumn(T_AUTHOR, verbose_name="Автор", orderable=False)

    T_ACTIONS = '''
                <a href="{% url 'manage-report-view' record.project.id %}"><i class="fas fa-eye"></i></a>
            '''
    actions = tables.TemplateColumn(T_ACTIONS, verbose_name="", orderable=False)
    updated_on = tables.Column(verbose_name="Дата изменения", orderable=False)

    class Meta:
        model = Report
        fields = (
            'status', 'project__id', 'project__title', 'project__budget_request_sum', 'project__author', 'updated_on',
            'actions')
        attrs = {"class": "table table-sm table-hover data-table table-responsive"}


class ReportingTable(tables.Table):
    # id = tables.LinkColumn('user-view-project', args=[A('pk')], verbose_name="№ Заявки")
    title = tables.LinkColumn('user-view-project', args=[A('pk')], orderable=False)
    budget_request_sum = tables.Column(verbose_name="Запрашиваемая сумма (руб.)", orderable=False)
    # averange_score = tables.Column(verbose_name="Средний балл", orderable=False)
    # delete = tables.TemplateColumn(T_DELETE, verbose_name="Удалить", orderable=False)
    org = tables.Column(verbose_name='Наименование Грантаполучателя', accessor='organization__short_name', orderable=False)
    inn = tables.Column(verbose_name='ИНН Грантаполучателя', accessor='organization__inn', orderable=False)
    # reportperiod = tables.Column(verbose_name='Дата сдачи отчетности по Соглашению', accessor='contest__reportperiod__date', orderable=False)
    reportperiod = tables.Column(default=None, empty_values=(), orderable=False, verbose_name='Дата сдачи отчетности по Соглашению')
    additionalagreements = tables.Column(default=None, empty_values=(), orderable=False, verbose_name='Дополнительное соглашение')
    report_accept_date = tables.Column(orderable=False)

    class Meta:
        model = Project
        fields = ('report_status', 'org', 'inn', 'title', 'budget_request_sum', 'reportperiod', 'additionalagreements',
                  'report_accept_date')
        attrs = {"class": "table table-sm table-hover data-table table-responsive"}

    def render_additionalagreements(self, value, record):
        s = ''
        for i in range(record.get_additional_agreements_count()):
            s += '+'
        return s

    def render_reportperiod(self, value, record):
        if record.report_date:
            return record.report_date
        try:
            return record.contest.reportperiod.date
        except:
            return '-'

