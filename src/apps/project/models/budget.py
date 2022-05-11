import uuid

from django.db import models


class GenericCost(models.Model):
    """
    расходы
    """
    TYPE_SALARY = 'salary'
    TYPE_INSURANCE = 'insurance'
    TYPE_PAYOUTS = 'payouts'
    TYPE_OFFICE = 'office'
    TYPE_TRAVEL = 'travel'
    TYPE_EQUIPMENT = 'equipment'
    TYPE_DEVEL = 'devel'
    TYPE_LEGAL = 'legal'
    TYPE_EVENTS = 'events'
    TYPE_PUBLISHING = 'publishing'
    TYPE_OTHER = 'other'

    TYPE = (
        (TYPE_SALARY, 'Оплата труда штатных работников'),
        (TYPE_PAYOUTS, 'Выплаты физическим лицам (за исключением индивидуальных предпринимателей) оказание ими услуг (выполнение работ) по гражданско-правовым договорам'),
        (TYPE_INSURANCE, 'Страховые взносы'),
        (TYPE_OFFICE, 'Офисные расходы'),
        (TYPE_TRAVEL, 'Командировочные расходы'),
        (TYPE_EQUIPMENT, 'Приобретение, аренда специализированного оборудования, инвентаря и сопутствующие расходы'),
        (TYPE_DEVEL, 'Разработка и поддержка сайтов, информационных систем и иные аналогичные расходы'),
        (TYPE_LEGAL, 'Оплата юридических, информационных, консультационных услуг и иные аналогичные расходы'),
        (TYPE_EVENTS, 'Расходы на проведение мероприятий'),
        (TYPE_PUBLISHING, 'Издательские, полиграфические и сопутствующие расходы'),
        (TYPE_OTHER, 'Прочие прямые расходы'),
    )

    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    type = models.CharField(
        max_length=32,
        choices=TYPE,
        verbose_name='Тип'
    )

    project = models.ForeignKey(
        'project.Project', verbose_name="Проект",
        on_delete=models.CASCADE
    )
    name = models.TextField("Наименование расходов")
    cost = models.DecimalField(
        "Стоимость единицы (в рублях)", max_digits=20, decimal_places=2)
    items_count = models.IntegerField(
        "Кол-во единиц")
    co_financing = models.DecimalField(
        "Софинансирование (по всем командируемым, в рублях)", max_digits=20, decimal_places=2)
    comment = models.TextField("Комментарий")

    def total(self):
        return self.cost * self.items_count

    def request_total(self):
        return self.cost * self.items_count - self.co_financing

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Расходы проекта"
        verbose_name_plural = "Расходы проекта"