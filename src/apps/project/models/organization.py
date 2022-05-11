from django.contrib.postgres.fields import JSONField
from django.core.validators import validate_email
from django.db import models
import logging as log


class Organization(models.Model):
    ogrn = models.CharField("ОГРН", max_length=255, blank=True)
    inn = models.CharField("ИНН", max_length=255, blank=True)
    kpp = models.CharField("КПП", max_length=255, blank=True)
    full_name = models.TextField("Полное название организации", blank=True)
    short_name = models.TextField("Сокращенное название организации", blank=True)
    registration_date = models.DateField("Дата регистрации", null=True, blank=True)
    address = models.CharField("Адрес (место нахождения) организации", max_length=255, blank=True)
    fact_address = models.CharField("Фактическое место нахождения организации", max_length=255, blank=True)
    legal_address = models.CharField("Адрес для направления организации юридически значимых сообщений", max_length=255, blank=True)
    main_activities = JSONField(default=list,null=True,blank=True)
    phone = models.CharField("Контактный телефон организации", max_length=20, blank=True)
    legal_email = models.CharField("Адрес электронной почты для направления организации юридически значимых сообщений", max_length=100, blank=True, validators=[validate_email])
    email = models.CharField("Адрес электронной почты для внешних коммуникаций", max_length=100, blank=True, validators=[validate_email])
    web = models.CharField("Веб-сайт", max_length=100, blank=True)
    social = models.TextField("Группы в соц. сетях", blank=True)
    manager_fio = models.CharField("ФИО руководителя организации", max_length=255, blank=True)
    manager_correct = models.BooleanField("Данные о руководителе совпадают с данными ЕГРЮЛ", blank=True, default=True)
    manager_position = models.CharField("Должность руководителя организации", max_length=255, blank=True)
    manager_birth_date = models.DateField("Дата рождения руководителя", null=True, blank=True)

    #Лица, имеющие право подписи без доверенности:
    trusted_persons  = JSONField(default=list,null=True,blank=True)

    #Руководители коллегиального органа управления организации:
    collegial_managers  = JSONField(default=list,null=True,blank=True)
    
    #Главный бухгалтер:
    accountant = JSONField(null=True,blank=True)

    #Иностранные граждане-учредители:
    foreign_founders  = JSONField(default=list,null=True,blank=True)

    #Юридические лица-учредители:
    legal_founders  = JSONField(default=list,null=True,blank=True)

    #Обособленные структурные подразделения организации-заявителя :
    structural_units  = JSONField(default=list,null=True,blank=True)

    #Участие (членство) в других некоммерческих организациях:
    non_commercial_organizations = JSONField(default=list,null=True,blank=True)

    #Участие в коммерческих организациях:
    commercial_organizations = JSONField(default=list,null=True,blank=True)

    members_count = models.IntegerField("Количество членов (участников) организации: физических лиц, юридических лиц:", default=0)

    employees_count = models.IntegerField("Количество штатных работников", default=0)
    volunteers_count = models.IntegerField("Количество добровольцев", default=0)

    # Доходы организации за предыдущий год:
    presidential_grants = models.DecimalField("президентские гранты", max_digits=20, decimal_places=2, default=0)
    non_commercial_grants = models.DecimalField("гранты, взносы, пожертвования российских некоммерческих организаций (исключая президентские гранты)", 
        max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    commercial_grants = models.DecimalField("взносы, пожертвования российских коммерческих организаций", max_digits=20, decimal_places=2, default=0)
    membership_fee = models.DecimalField("вступительные, членские и иные взносы, пожертвования российских граждан", max_digits=20, decimal_places=2,  default=0)
    foreign_grants = models.DecimalField("гранты, взносы, пожертвования иностранных организаций и иностранных граждан", max_digits=20, decimal_places=2, default=0)
    federal_budget = models.DecimalField("средства, полученные из федерального бюджета", max_digits=20, decimal_places=2, default=0)
    region_budget = models.DecimalField("средства, полученные из бюджетов субъектов Российской Федерации", max_digits=20, decimal_places=2, default=0)
    local_budget = models.DecimalField("средства, полученные из местных бюджетов", max_digits=20, decimal_places=2, default=0)
    revenue = models.DecimalField("доходы (выручка) от реализации товаров, работ, услуг, имущественных прав", default=0, max_digits=20, decimal_places=2)
    dividends = models.DecimalField("внереализационные доходы (дивиденды, проценты по депозитам и т.п.)", max_digits=20, decimal_places=2, default=0)
    other_income = models.DecimalField("прочие доходы", max_digits=20, decimal_places=2, default=0)

    total_cost = models.DecimalField("Общая сумма расходов организации за предыдущий год", max_digits=20, decimal_places=2,  default=0)
    beneficiaries_count = models.IntegerField("Количество благополучателей за предыдущий год (с января по декабрь): физические лица, юридические лица", null=True, blank=True)
    
    #Основные реализованные проекты и программы за последние 5 лет:
    success_projects = JSONField(default=list,null=True,blank=True)
    
    #Имеющиеся в распоряжении организации материально-технические ресурсы:
    material_resources = JSONField(null=True,blank=True)

    media_publications = models.TextField("Публикации в СМИ", null=True, blank=True)

    TYPE_1 = 'type1'
    TYPE_2 = 'type2'

    TYPE = (
        (TYPE_1, 'Организация состоит в реестре исполнителей общественно-полезных услуг Минюста'),
        (TYPE_2, 'Организация оказывает информационную, консультационную, методическую, образовательную, экспертную и иную поддержку социально ориентированным некоммерческим организациям'),
    )

    support_type = models.CharField(
        max_length=32,
        choices=TYPE,
        verbose_name='Приоритетная поддержка организации',
        null=True, blank=True
    )

    checklist = JSONField(null=True,blank=True)

    def geography_str(self):
        s = ''
        for g in self.geography_set.all():
            s += g.name + '; '

        return s

    def have_checklist(self):
        for x in self.checklist:
            log.error(x['value'])
            if x['value'] == False:
                return True

        return False


    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = "Организация заявитель"
        verbose_name_plural = "Организации заявители"
