from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase

from apps.expert.models import Expert
from django.apps import apps


class Direction(models.Model):
    title = models.TextField("Название")
    slug = models.SlugField(max_length=160, unique=True, verbose_name="ЧПУ")
    img = models.ImageField(upload_to='directions', verbose_name="Картинка")
    max_sum = models.DecimalField("Максимальная сумма бюджета гранта", max_digits=20, decimal_places=2, null=True,
                                  blank=True)

    def subjects(self):
        return Subject.objects.filter(direction_id=self.id)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Направление конкурса"
        verbose_name_plural = "Направления конкурса"
        ordering = ['title']


class Subject(models.Model):
    title = models.TextField("Название")
    order_field = models.IntegerField()
    direction = models.ForeignKey(
        Direction, verbose_name="Направление", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тематику направления"
        verbose_name_plural = "Тематики направления"


class Contest(models.Model):
    NEW = 'new'
    OPENED = 'opened'
    TECH_WORK = 'tech_work'
    CHECK = 'check'
    ON_EXAM = 'on_exam'
    CLOSED = 'closed'

    STATUS = (
        (NEW, 'Новый'),
        (OPENED, 'Идет прием заявок'),
        (TECH_WORK, 'Идут подготовительные работы'),
        (CHECK, 'Идет проверка'),
        (ON_EXAM, 'Идет независимая экспертиза'),
        (CLOSED, 'Конкурс завершен'),
    )

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=NEW,
        verbose_name='Статус'
    )

    title = models.CharField("Название конкурса", max_length=255)
    content = models.TextField("Описание")
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Expert, verbose_name="Автор", on_delete=models.CASCADE)
    directions = models.ManyToManyField(Direction, verbose_name="Направления")

    def report_remaining_days(self):
        from datetime import datetime
        return (self.reportperiod.date - datetime.now().date()).days

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Конкурс"
        verbose_name_plural = "Конкурсы"


class Criteria(models.Model):
    title = models.CharField("Критерии оценки заявок на участие в конкурсе", max_length=255)
    info = models.TextField("Информация по порядку выставления баллов", null=True, blank=True)

    def __str__(self):
        return self.title

    #TODO: Какого черта здесь происходит подсчет, надо перенести
    def project_score(self, project_id):
        model = apps.get_model('project', 'Project')
        project = model.objects.get(pk=project_id)

        sc_sum = 0
        sc_count = 0
        for score_sheet in project.scoresheet_set.all():
          sc_count += 1
          sc_sum += score_sheet.criteria_score_sum(self.id) # Без учета коэффициента
        score = sc_sum / sc_count
        return score

    class Meta:
        verbose_name = "Критерий оценки"
        verbose_name_plural = "Критерии оценки"


class Coefficient(models.Model):
    criteria = models.ForeignKey(
        Criteria, verbose_name="Критерий оценки", on_delete=models.CASCADE
    )
    contest = models.ForeignKey(
        Contest, verbose_name="Конкурс", on_delete=models.CASCADE
    )
    col500 = models.DecimalField(
        "не более 500тыс. рублей", max_digits=4, decimal_places=2)
    col1000 = models.DecimalField(
        "свыше 500 тыс. рублей и не более 1 млн рублей", max_digits=4, decimal_places=2)
    col3000 = models.DecimalField(
        "свыше 1 млн рублей и не более 3 млн рублей", max_digits=4, decimal_places=2)
    colinf = models.DecimalField(
        "свыше 3 млн рублей", max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = "Коэффициент значимости"
        verbose_name_plural = "Коэффициенты значимости"
        ordering = ['criteria__title']


class ScoreSheet(models.Model):
    """Оценочный лист"""

    NEW = 'new'
    FINISHED = 'finished'

    STATUS = (
        (NEW, 'На экспертизе'),
        (FINISHED, 'Завершен'),
    )

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=NEW,
        verbose_name='Статус'
    )

    contest = models.ForeignKey(
        Contest, verbose_name="Конкурс", on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        'project.Project', verbose_name="Проект", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User, verbose_name="Автор", on_delete=models.CASCADE)
    updated_on = models.DateTimeField("Обновлен", auto_now=False)
    created_on = models.DateTimeField("Создан", auto_now_add=True)

    additional_score1 = models.DecimalField(
        "Если организация состоит в реестре исполнителей общественно полезных услуг", default=0, max_digits=5,
        decimal_places=0)
    additional_score2 = models.DecimalField(
        "Если Заявитель является организацией, оказывающей информационную, "
        "консультационную, методическую, образовательную, экспертную и иную поддержку "
        "социально ориентированным некоммерческим организациям, возглавляющим рейтинг "
        "эффективности деятельности за предыдущий отчетный период, "
        "разработанного Уполномоченным органом, размещаемом на Портале",
        default=0, max_digits=5, decimal_places=0, blank=True)

    RESULT_GOOD = 'good'
    RESULT_NO_BAD = 'no_bad'
    RESULT_BAD = 'bad'

    RESULT = (
        (RESULT_GOOD, 'проект хороший и безусловно рекомендуется к поддержке'),
        (RESULT_NO_BAD,
         'проект в целом неплохой, но в нем есть недочеты, которые не позволяют сделать однозначный вывод о целесообразности поддержки проекта'),
        (RESULT_BAD, 'проект не рекомендуется к поддержке'),
    )

    result = models.CharField(
        max_length=32,
        choices=RESULT,
        verbose_name='Вывод',
        null=True,
        blank=True
    )

    def score_sum(self):
        s = Score.objects.filter(score_sheet_id=self.id).aggregate(models.Sum('score'))

        return s['score__sum']

    score_sum.short_description = 'Оценка эксперта'

    def criteria_score_sum(self, criteria_id):
        s = Score.objects.filter(score_sheet_id=self.id, criteria_id=criteria_id).aggregate(models.Sum('score'))
        return s['score__sum']

    def score_total_sum(self):
        sum = self.additional_score1 + self.additional_score2
        for score in self.score_set.all():
            sum = sum + score.score * score.coefficient()
        return round(sum, 2)

    score_total_sum.short_description = 'Оценка с коэффициентом и дополнительными баллами'

    def __str__(self):
        return "Экспертиза от " + self.author.username + " проекта " + self.project.title

    class Meta:
        verbose_name = "Оценочный лист"
        verbose_name_plural = "Оценочные листы"
        ordering = ['-created_on']


class Score(models.Model):
    score_sheet = models.ForeignKey(
        ScoreSheet, verbose_name="Оценочный лист", on_delete=models.CASCADE
    )
    criteria = models.ForeignKey(
        Criteria, verbose_name="Критерий оценки", on_delete=models.CASCADE
    )
    score = models.DecimalField("Оценка", max_digits=2, decimal_places=0)
    comment = models.TextField("Комментарий", null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def coefficient(self):
        budget_request_sum = self.score_sheet.project.budget_request_sum()
        coefficient = Coefficient.objects.get(criteria_id=self.criteria_id, contest_id=self.score_sheet.contest_id)

        if budget_request_sum <= 500000:
            k = coefficient.col500
        elif 500000 < budget_request_sum <= 1000000:
            k = coefficient.col1000
        elif 1000000 < budget_request_sum <= 3000000:
            k = coefficient.col3000
        else:
            k = coefficient.colinf

        return k

    def __str__(self):
        return self.criteria.title + ": " + str(self.score)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ['criteria__title']


class ReportPeriod(models.Model):
    contest = models.OneToOneField(Contest, verbose_name="Конкурс", on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата')
    notified = models.BooleanField(verbose_name='Уведомленены', default=False)

    class Meta:
        verbose_name = "Срок сдачи отчетности"
        verbose_name_plural = "Сроки сдачи отчетности"


class DocumentTag(TagBase):
    system = models.CharField(max_length=255, verbose_name='System name')
    is_hidden = models.BooleanField(default=False, verbose_name='Скрытый тэг')

    class Meta:
        verbose_name = 'Тэг документа'
        verbose_name_plural = 'Тэги документа'


class TaggedDocument(GenericTaggedItemBase):
    tag = models.ForeignKey(
        DocumentTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
        # related_name="%(app_label)s_%(class)s_items",
    )


class Document(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    file = models.FileField(verbose_name='Файл', blank=False)
    tags = TaggableManager(through=TaggedDocument, blank=False)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Конкурс')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'

    def __str__(self):
        return self.title


class Commission(models.Model):
    photo = models.ImageField(upload_to='commission', verbose_name="Фото")
    fio = models.CharField(max_length=255, verbose_name='ФИО')
    position = models.TextField(verbose_name="Должность")
    order_field = models.IntegerField(verbose_name="Порядок", null=True, blank=True)
    boss = models.BooleanField(verbose_name="Руководитель", default=False)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "члена комиссии"
        verbose_name_plural = "Координационная комиссия"