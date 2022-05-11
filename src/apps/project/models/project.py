import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, F
from vote.models import VoteModel

from apps.contest.models import Direction, Subject, Contest
from apps.expert.models import Expert
from .organization import Organization
from .project_manager import ProjectManager
from .project_percent_mixin import ProjectPercentMixin
from .reporting import AgreementFile
import logging as log



class Project(VoteModel, models.Model, ProjectPercentMixin):
    DRAFT = 'draft'
    NEW = 'new'
    ON_CHECK = 'on_check'
    FIX = 'fix'
    ON_EXAM = 'on_exam'
    WIN = 'win'
    NOT_WIN = 'not_win'
    REJECT = 'reject'

    STATUS = (
        (DRAFT, 'Черновик'),
        (NEW, 'Подана'),
        (ON_CHECK, 'На проверке'),
        (FIX, 'На доработку'),
        (ON_EXAM, 'На экспертизе'),
        (WIN, 'Победитель конкурса'),
        (NOT_WIN, 'Проект, не получивший поддержку'),
        (REJECT, 'Отклонена'),
    )

    REPORT_REALIZATION = 'realization'
    REPORT_EXPIRE = 'expire'
    REPORT_CHECK = 'check'
    REPORT_COMPLETION = 'completion'
    REPORT_ACCEPT = 'accept'

    REPORT_STATUS = (
        (REPORT_REALIZATION, 'Реализуется'),
        (REPORT_EXPIRE, 'Не сдан'),
        (REPORT_CHECK, 'На проверке'),
        (REPORT_COMPLETION, 'На доработке'),
        (REPORT_ACCEPT, 'Принят')
    )

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=DRAFT,
        verbose_name='Статус'
    )

    report_status = models.CharField(max_length=32, choices=REPORT_STATUS, default=REPORT_REALIZATION, verbose_name='Статус отчетности')
    report_date = models.DateField(verbose_name='Срок сдачи отчетности', default=None, blank=True, null=True)

    contest = models.ForeignKey(
        Contest, verbose_name="Конкурс",
        on_delete=models.CASCADE, null=True, blank=True
    )
    direction = models.ForeignKey(
        Direction,
        verbose_name="Грантовое направление, которому преимущественно соответствует планируемая деятельность по проекту",
        on_delete=models.CASCADE, null=True, blank=True
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name="Тематика грантового направления, которому преимущественно соответствует планируемая деятельность по проекту",
        on_delete=models.CASCADE, null=True, blank=True
    )

    manager = models.ForeignKey(
        ProjectManager, verbose_name="Менеджер проекта",
        on_delete=models.CASCADE, null=True, blank=True
    )

    organization = models.ForeignKey(
        Organization, verbose_name="Организация заявитель",
        on_delete=models.CASCADE, null=True, blank=True
    )

    title = models.TextField("Название проекта", blank=True)
    description = models.TextField("Краткое описание проекта (деятельности в рамках проекта)", blank=True)

    start_date = models.DateField("Дата начала реализации проекта", null=True, blank=True)
    finish_date = models.DateField("Дата окончания реализации проекта", null=True, blank=True)
    social_significance = models.TextField("Обоснование социальной значимости проекта", blank=True)
    info_support = models.TextField("Как будет организовано информационное сопровождение проекта", blank=True)
    quality_results = models.TextField("Качественные результаты", blank=True)
    further_progress = models.TextField("Дальнейшее развитие проекта", blank=True)
    sources = models.TextField("Источники ресурсного обеспечения проекта в дальнейшем", blank=True)

    updated_on = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)
    created_on = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    request_date = models.DateTimeField(verbose_name="Дата подачи", null=True, blank=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    experts = models.ManyToManyField(Expert, verbose_name="Эксперты", related_name='experts', blank=True)
    request_file = models.FileField(upload_to='projects/%s' % datetime.date.today().year, verbose_name="Файл", null=True, blank=True)
    best = models.BooleanField(verbose_name="Лучший проект", default=False)
    report_accept_date = models.DateField("Дата принятия отчета", null=True, blank=True, default=None)


    def can_edit(self):
        return (self.status == self.DRAFT or self.status == self.FIX) and (self.contest.status == self.contest.OPENED or self.contest.status == self.contest.TECH_WORK)

    def score_sheets_has_finished(self):
        finished = False
        for score_sheet in self.scoresheet_set.all():
            if score_sheet.status == score_sheet.FINISHED:
                finished = True

        return finished

    def averange_score(self):
        score_sheets = self.scoresheet_set.all()
        sc = len(score_sheets)
        sum = 0
        for sheet in score_sheets:
            sum = sum + sheet.score_total_sum()

        return round(sum / sc if sc > 0 else 0, 2)

    def avg_additional_score(self):
        score_sheets = self.scoresheet_set.all()
        sc = len(score_sheets)
        sum = 0
        for sheet in score_sheets:
            sum = sum + sheet.additional_score1 + sheet.additional_score2

        return round(sum / sc if sc > 0 else 0, 2)

    def co_finance_percent(self):
        if self.budget_sum() == 0:
            return 0
        budget_sum = self.budget_sum()
        if budget_sum == 0:
            return 0.00
        return round(self.budget_co_financing_sum() * 100 / budget_sum, 2)

    def budget_sum(self):
        sum = self.genericcost_set.aggregate(
            total=Sum(F('cost') * F('items_count'), output_field=models.DecimalField())
        )['total']

        return sum if sum else 0

    def budget_sum_by_type(self, t):
        sum = self.genericcost_set.filter(type=t).aggregate(
            total=Sum(F('cost') * F('items_count'), output_field=models.DecimalField())
        )['total']

        return sum if sum else 0

    def budget_request_sum(self):
        sum = self.genericcost_set.aggregate(
            total=Sum(F('cost') * F('items_count') - F('co_financing'), output_field=models.DecimalField())
        )['total']

        return sum if sum else 0

    def budget_request_sum_by_type(self, t):
        sum = self.genericcost_set.filter(type=t).aggregate(
            total=Sum(F('cost') * F('items_count') - F('co_financing'), output_field=models.DecimalField())
        )['total']

        return sum if sum else 0

    def budget_co_financing_sum_by_type(self, t):
        sum = self.genericcost_set.filter(type=t).aggregate(
            total=Sum(F('co_financing'), output_field=models.DecimalField())
        )['total']

        return sum if sum else 0

    def budget_co_financing_sum(self):
        sum = self.genericcost_set.aggregate(
            total=Sum(F('co_financing'), output_field=models.DecimalField())
        )['total']

        return sum if sum else 0

    def geography_list(self):
        return self.geography_set.all().filter(organization_id__isnull=True)

    def presentation_files(self):
        return self.projectfile_set.all().filter(type='presentation')

    def letter_files(self):
        return self.projectfile_set.all().filter(type='letter')

    def manager_letter_files(self):
        return self.projectfile_set.all().filter(type='manager')

    def manager_photo_files(self):
        return self.projectfile_set.all().filter(type='manager_photo')

    def organization_egrul_files(self):
        return self.projectfile_set.all().filter(type='organization_egrul')

    def organization_nalog_files(self):
        return self.projectfile_set.all().filter(type='organization_nalog')

    def organization_sogr_files(self):
        return self.projectfile_set.all().filter(type='organization_sogr')

    def organization_minust_files(self):
        return self.projectfile_set.all().filter(type='organization_minust')

    def organization_ustav_files(self):
        return self.projectfile_set.all().filter(type='organization_ustav')

    def organization_etc_files(self):
        return self.projectfile_set.all().filter(type='organization_etc')

    def target_groups(self):
        return self.targetgroup_set.all().filter(type='project')

    def organization_target_groups(self):
        return self.targetgroup_set.all().filter(type='organization')

    def internal_comments(self):
        return self.comment_set.all().filter(type='internal')

    def external_comments(self):
        return self.comment_set.all().filter(type='external')

    def score_sheet(self):
        return self.scoresheet_set.get(project=self)

    def comments_str(self):
        s = ''
        for c in self.comment_set.filter(type='internal').all():
            s += c.content + '\n'

        return s

    def checklist_str(self):
        s = ''
        from apps.project.services import OrganizationValidate
        #self.organization.checklist = OrganizationValidate(self.organization, None).toJSON()
        checklist = OrganizationValidate(self.organization, None).toJSON()
        for c in checklist:
            if c['value'] == False:
                s += c['message'] + ' ' + c['comment'] + ';\n\n'

        return s

    def report_status_name(self):
        for s in self.REPORT_STATUS:
            if s[0] == self.report_status:
                return s[1]
        return None

    def is_have_agreements(self):
        for a in self.agreementfile_set.all():
            if a.type == AgreementFile.TYPE_AGREEMENT:
                return True
        return False

    def is_have_additional_agreements(self):
        for a in self.agreementfile_set.all():
            if a.type == AgreementFile.TYPE_ADDITIONAL_AGREEMENT:
                return True
        return False

    def get_agreements(self):
        a_s = []
        for a in self.agreementfile_set.all():
            if a.type == AgreementFile.TYPE_AGREEMENT:
                a_s.append(a)
        return a_s

    def get_additional_agreements(self):
        a_s = []
        for a in self.agreementfile_set.all():
            if a.type == AgreementFile.TYPE_ADDITIONAL_AGREEMENT:
                a_s.append(a)
        return a_s

    def get_additional_agreements_count(self):
        return self.agreementfile_set.filter(type=AgreementFile.TYPE_ADDITIONAL_AGREEMENT).count()

    def get_check_results(self):
        a_s = []
        for a in self.agreementfile_set.all():
            if a.type == AgreementFile.TYPE_CHECK_RESULTS:
                a_s.append(a)
        return a_s

    def is_has_report(self):
        return self.status == 'win'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ['-created_on']

Project._meta.get_field('id').verbose_name = '№ заявки'
