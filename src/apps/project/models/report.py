from django.contrib.postgres.fields import JSONField
from django.db import models

class Report(models.Model):
    content = models.TextField("Отчет", blank=True, null=True)
    project = models.OneToOneField(
        'project.Project',
        verbose_name="Проект",
        primary_key=True,
        on_delete=models.CASCADE
    )

    DRAFT = 'draft'
    NEW = 'new'
    FIX = 'fix'
    APPROVED = 'approved'
    REJECT = 'reject'

    STATUS = (
        (DRAFT, 'Черновик'),
        (NEW, 'На проверке'),
        (FIX, 'На доработку'),
        (REJECT, 'Отклонена'),
        (APPROVED, 'Принят'),
    )

    status = models.CharField(
        max_length=32,
        choices=STATUS,
        default=DRAFT,
        verbose_name='Статус'
    )

    """ Смета реализации проекта """
    smeta = JSONField(default=list, null=True, blank=True)

    """
    ОТЧЕТ
    о расходах, источником финансового обеспечения
    которых является субсидии из государственного
    бюджета на государственную поддержку социально
    ориентированных некоммерческих организаций
    """
    cost = JSONField(default=dict, null=True, blank=True)

    """
    ОТЧЕТ

    о достижении значений показателей результативности
    предоставления субсидии из государственного
    бюджета на государственную поддержку социально
    ориентированных некоммерческих организаций
    """
    result = JSONField(default=dict, null=True, blank=True)

    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    request_date = models.DateTimeField(null=True, blank=True)

    def smeta_cost_sum(self):
        cost_sum = 0
        for item in self.smeta:
            cost_sum += int(item['cost']) * int(item['items_count'])

        return cost_sum

    def smeta_from_budget_sum(self):
        sum = 0
        for item in self.smeta:
            sum += int(item['from_budget'])

        return sum
        
    def smeta_co_finance_sum(self):
        sum = 0
        for item in self.smeta:
            sum += int(item['co_financing'])

        return sum

    def smeta_request_sum(self):
        return self.smeta_cost_sum() - self.smeta_co_finance_sum()


    def cost_cost_sum(self):
        cost_sum = 0
        for item in self.smeta:
            cost_sum += int(item['cost'])

        return cost_sum

    def cost_social_sum(self):
        cost_sum = 0
        for item in self.cost['social_items']:
            cost_sum += int(item['cost'])

        return cost_sum

    def cost_reestr_sum(self):
        cost_sum = 0
        for item in self.cost['reestr_items']:
            cost_sum += int(item['cost'])

        return cost_sum

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Отчет по проекту"
        verbose_name_plural = "Отчеты по проекту"