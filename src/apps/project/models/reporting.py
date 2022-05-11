import datetime

from django.db import models
from urllib.parse import unquote


class ReportingBest(models.Model):
    project = models.ForeignKey('project.Project', verbose_name="Проект", on_delete=models.CASCADE, related_name='bests')
    description = models.TextField("Краткое описание исполнения проекта со следующими пояснениями: Необходимо загрузить текст на русском языке, состоящий из не более 3000 знаков содержащий краткое описание реализации проекта (- цели, задачи, - описание проекта,- руководитель проекта,- предыстория реализации проекта, - дальнейшее развитие проекта, - какие мероприятия проведены, - кто участвовал в реализации инициативы и др.). ")
    beneficiaries_count = models.IntegerField("Количество благополучателей по итогам реализации проекта", default=0)
    volunteers_count = models.IntegerField("Количество добровольцев, привлеченных к реализации проекта", default=0)
    self_co_financing = models.DecimalField("Размер софинансирования проекта из собственных средств", decimal_places=2, max_digits=20, default=0)
    targets = models.TextField("Достижение целевых показателей (Краткая информация о достижении показателей указанных в соглашении)")
    additional_amount = models.DecimalField("Объем средств, дополнительно привлеченных на реализацию проекта (включая примерную оценку труда добровольцев, безвозмездно полученных товаров, работ, услуг, имущественных прав) с краткой аналитической информацией об источнике финансирования", decimal_places=2, max_digits=20, default=0)
    links = models.TextField(
        "Информационная открытость организации, освещение мероприятий проекта. Загружаются активные ссылки на статьи, сюжеты о мероприятиях проекта, размещенные в интернет ресурсах, а также наименование и выходные данные размещенные в печатных изданиях, журналах, газетах.")

    def get_photos(self):
        photos = []
        for f in self.files.all():
            if f.type == 0:
                photos.append(f)
        return photos

"""
Фотографии о реализации проекта в формате pdf в количестве не менее 5 шт.
"""
class ReportingBestFile(models.Model):
    TYPES = ((0, 'photo'), (1, 'doc'))

    reporting_best = models.ForeignKey(ReportingBest, on_delete=models.CASCADE, related_name='files')
    type = models.PositiveSmallIntegerField(choices=TYPES)
    file = models.FileField(upload_to='projects/reports/%s' % datetime.date.today().year, verbose_name="Файл")

    class Meta:
        pass

    def get_name(self):
        return unquote(self.file.url.split('/').pop())


class ReportingEvent(models.Model):
    project = models.ForeignKey('project.Project', verbose_name="Проект", on_delete=models.CASCADE, related_name='reporting_events')
    name = models.TextField("Мероприятие, его содержание, место проведения", max_length=1000)
    start_date = models.DateField("Дата начала")
    finish_date = models.DateField("Дата окончания")
    fulfillment = models.CharField(max_length=10000)

    class Meta:
        ordering = ['pk']

    def get_photos(self):
        photos = []
        for f in self.files.all():
            if f.type == 0:
                photos.append(f)
        return photos

    def get_docs(self):
        docs = []
        for f in self.files.all():
            if f.type == 1:
                docs.append(f)
        return docs


class ReportingEventFile(models.Model):
    TYPES = ((0, 'photo'), (1, 'doc'))

    reporting_event = models.ForeignKey(ReportingEvent, on_delete=models.CASCADE, related_name='files')
    type = models.PositiveSmallIntegerField(choices=TYPES)
    file = models.FileField(upload_to='projects/reports/%s' % datetime.date.today().year, verbose_name="Файл")

    class Meta:
        pass

    def get_name(self):
        return unquote(self.file.url.split('/').pop())


class ReportingEventLink(models.Model):
    reporting_event = models.ForeignKey(ReportingEvent, on_delete=models.CASCADE, related_name='links')
    url = models.URLField(max_length=255)


class ReportingIndicator(models.Model):
    TYPES = (
        ('1', False, 'Количество граждан, принявших участие в реализации мероприятий проекта, в том числе', 'Человек', 792),
        ('1.1', True, 'Количество привлеченных добровольцев (волонтеров) к реализации проекта', 'Единица', 642),
        ('2', True, 'Количество благополучателей проекта', 'Человек', 792),
        ('3', False, 'Количество территорий охваченные мероприятиями проекта, в том числе', 'Единица', 642),
        ('3.1', True, 'муниципальные районы', 'Единица', 642),
        ('3.2', True, 'городские округа', 'Единица', 642),
        ('3.3', True, 'городские населенные пункты', 'Единица', 642),
        ('3.4', True, 'сельские поселения', 'Единица', 642),
        ('4', False, 'Количество трудоустроенных граждан в реализации мероприятий проекта, в том числе', 'Человек', 792),
        ('4.1', True, 'по трудовому договору', 'Человек', 792),
        ('4.2', True, 'по договору гражданско-правового характера', 'Человек', 792),
        ('6', False, 'Количество публикаций в средствах массовой информации о мероприятиях проекта, в том числе', 'Единица', 642),
        ('6.1', True, 'информационные сайты', 'Единица', 642),
        ('6.2', True, 'телевидение', 'Единица', 642),
        ('6.3', True, 'радио', 'Единица', 642),
        ('6.4', True, 'печатные издания (газеты, журналы)', 'Единица', 642),
        ('6.5', True, 'социальные сети (Instagram Vkontakte Facebook и прочее)', 'Единица', 642),
        ('7', True, 'Количество мероприятий, проведенных в рамках реализации проекта', 'Единица', 642)
    )

    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='indicators')
    type = models.CharField(max_length=10)
    date = models.DateField(blank=True, null=True, default=None)
    planned = models.IntegerField(blank=True, null=True, default=None)
    value = models.IntegerField(blank=True, null=True, default=None)
    reason = models.CharField(max_length=1000, blank=True, null=True, default=None)

    @classmethod
    def get_for_project(cls, project):
        d = {}
        for i in cls.objects.filter(project=project).all():
            d[i.type] = i
        if len(d) == 0:
            for t in cls.TYPES:
                if t[1]:
                    m = ReportingIndicator()
                    m.type = t[0]
                    m.project = project
                    m.save()
                    d[t[0]] = m
        return d

    def get_photos(self):
        photos = []
        for f in self.files.all():
            if f.type == 0:
                photos.append(f)
        return photos

    def get_docs(self):
        docs = []
        for f in self.files.all():
            if f.type == 1:
                docs.append(f)
        return docs


class ReportingIndicatorFile(models.Model):
    TYPES = ((0, 'photo'), (1, 'doc'))

    indicator = models.ForeignKey(ReportingIndicator, on_delete=models.CASCADE, related_name='files')
    type = models.PositiveSmallIntegerField(choices=TYPES)
    file = models.FileField(upload_to='projects/reports/%s' % datetime.date.today().year, verbose_name="Файл")

    class Meta:
        pass

    def get_name(self):
        return unquote(self.file.url.split('/').pop())


class ReportingIndicatorLink(models.Model):
    indicator = models.ForeignKey(ReportingIndicator, on_delete=models.CASCADE, related_name='links')
    url = models.URLField(max_length=255)


class ReportingExpense(models.Model):
    '''
    TYPES = (
        ('1', 'Оплата труда штатных работников, но не более 20% от общего размера Гранта), всего'),
        ('2', 'Уплата налогов, сборов, страховых взносов и иных платежей в бюджеты бюджетной системы Российской Федерации, но не более 10% от общего размера Гранта, всего:'),
        ('3', 'Оплата услуг привлеченных специалистов, сторонних организаций, но не более 5% от общего размера Гранта, всего'),
        ('4', 'Арендная плата, но не более 10% от общего размера Гранта, всего'),
        ('5', 'Командировочные расходы, всего'),
        ('6', 'Прямы расходы, непосредственно связанные с реализацией проекта, всего'),
        ('7', 'Средства софинансирования, всего'),
    )
    '''
    TYPES = (
        ('1', 'Оплата труда штатных работников'),
        ('2', 'Выплаты физическим лицам (за исключением индивидуальных предпринимателей) оказание ими услуг (выполнение работ) по гражданско-правовым договорам'),
        ('3', 'Страховые взносы'),
        ('4', 'Офисные расходы'),
        ('5', 'Командировочные расходы'),
        ('6', 'Приобретение, аренда специализированного оборудования, инвентаря и сопутствующие расходы'),
        ('7', 'Разработка и поддержка сайтов, информационных систем и иные аналогичные расходы'),
        ('8', 'Оплата юридических, информационных, консультационных услуг и иные аналогичные расходы'),
        ('9', 'Расходы на проведение мероприятий'),
        ('10', 'Издательские, полиграфические и сопутствующие расходы'),
        ('11', 'Прочие прямые расходы'),
    )
    project = models.ForeignKey('project.Project', on_delete=models.CASCADE, related_name='expenses')
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    qty = models.IntegerField(blank=True, null=True, default=None)
    unit_cost = models.DecimalField(blank=True, null=True, default=None, max_digits=12, decimal_places=2)
    overall = models.DecimalField(blank=True, null=True, default=None, max_digits=15, decimal_places=2)
    planned = models.DecimalField(blank=True, null=True, default=None, max_digits=15, decimal_places=2)
    value = models.DecimalField(blank=True, null=True, default=None, max_digits=15, decimal_places=2)

    @classmethod
    def get_for_project(cls, project):
        d = {}
        for i in cls.objects.filter(project=project).all():
            if not i.type in d:
                d[i.type] = []
            d[i.type].append(i)
        return d


class ReportingExpenseFile(models.Model):
    expense = models.ForeignKey(ReportingExpense, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='projects/reports/%s' % datetime.date.today().year, verbose_name="Файл")
    type = models.Field

    class Meta:
        pass

    def get_name(self):
        return unquote(self.file.url.split('/').pop())


class AgreementFile(models.Model):
    TYPE_AGREEMENT = 'agreement'
    TYPE_ADDITIONAL_AGREEMENT = 'additional_agreement'
    TYPE_CHECK_RESULTS = 'check_results'

    TYPE = (
        (TYPE_AGREEMENT, 'Соглашение'),
        (TYPE_ADDITIONAL_AGREEMENT, 'Дополнительное соглашение'),
        (TYPE_CHECK_RESULTS, 'Итоги проверки'),
    )

    project = models.ForeignKey('project.Project', verbose_name="Проект", on_delete=models.CASCADE)
    type = models.CharField(max_length=32, choices=TYPE, verbose_name='Тип')
    title = models.CharField(max_length=500, blank=False, verbose_name='Наименование')
    number = models.CharField(max_length=50, blank=False, verbose_name='Номер')
    date = models.DateField(blank=False, verbose_name='Дата подписания')
    file = models.FileField(upload_to='projects/agreements/%s' % datetime.date.today().year, verbose_name="Файл")

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'



