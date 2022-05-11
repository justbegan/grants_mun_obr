import datetime

from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter
from notifications.signals import notify

from .models import Project, Goal, ProjectManager, GenericCost, Partner, ProjectFile, Comment, Organization, QuantResult
from .models.reporting import AgreementFile


class ProjectFileAdminInline(admin.TabularInline):
    extra = 0
    model = ProjectFile


class AgreementFileAdminInline(admin.TabularInline):
    extra = 0
    model = AgreementFile


class GoalAdminInline(admin.TabularInline):
    extra = 0
    model = Goal


class PartnerAdminInline(admin.TabularInline):
    extra = 0
    model = Partner

class QuantResultAdminInline(admin.TabularInline):
    extra = 0
    model = QuantResult


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Проекты"""
    inlines = (ProjectFileAdminInline, AgreementFileAdminInline,
               GoalAdminInline, PartnerAdminInline, QuantResultAdminInline)
    list_display = ('id', 'title', 'status', 'score_sheets_count', 'assign_experts', 'voted_experts', 'direction', 'contest', 'user_name', 'email')
    search_fields = ['title', 'id']
    list_display_links = ('id', "title",)
    list_filter = (
        ('direction', RelatedDropdownFilter),
        ('contest', RelatedDropdownFilter),
        ('status', ChoiceDropdownFilter),
    )
    autocomplete_fields = ('author', )

    def user_name(self, obj):
        return  obj.author.username + '('+ obj.author.last_name + ' ' + obj.author.first_name + ')'
    user_name.short_description = 'Автор'

    def email(self, obj):
        return  obj.author.email
    email.short_description = 'email'

    def score_sheets_count(self, obj):
        return obj.scoresheet_count
    score_sheets_count.short_description = 'Кол-во оц. листов'
    score_sheets_count.admin_order_field = 'scoresheet_count'

    def assign_experts(self, obj):
        sd = ""
        for d in obj.experts.all().order_by('last_name'):
            sd = sd +  d.full_name() + '<br>'
        return format_html(sd)
    assign_experts.short_description = 'Назначенные эксперты'

    def voted_experts(self, obj):
        sd = ""
        for d in obj.scoresheet_set.all().order_by('author__last_name'):
            sd = sd +  d.author.last_name + ' ' + d.author.first_name + '<br>'
        return format_html(sd)
    voted_experts.short_description = 'Оценившие эксперты'

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(scoresheet_count=Count('scoresheet'))

    def save_model(self, request, obj, form, change):
        if change:
            prev = self.model.objects.get(id=obj.id)

            if obj.report_status != prev.report_status and obj.report_status == Project.REPORT_ACCEPT:
                obj.report_accept_date = datetime.date.today()

            super().save_model(request, obj, form, change)

            if obj.report_status != prev.report_status:
                text = 'Изменен статус отчётности проекта ' + obj.title + ' на ' + obj.report_status_name()
                notify.send(obj, recipient=obj.author, verb=text)
                from apps.project.services.notify import send_email_async
                html = 'Изменен статус отчётности проекта на: ' + obj.report_status_name()
                send_email_async(obj.title, html, [obj.author.email])


@admin.register(ProjectManager)
class ProjectMangerAdmin(admin.ModelAdmin):
    list_display = ('id', 'position', 'last_name', 'first_name', 'middle_name')


@admin.register(GenericCost)
class GenericCostAdmin(admin.ModelAdmin):
    list_display = ('project', 'type', 'name', 'cost',
                    'items_count', 'co_financing', 'comment')
    list_filter = ('project',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'status', 'content', 'created_on', 'author')
    search_fields = ['project__id']
    list_display_links = ('project_id', "content",)
    list_filter = ('project__status',)

    def status(self, obj):
        return  obj.project.get_status_display()
    status.short_description = 'Статус проекта'
    

@admin.register(Organization)
class ProjectOrganization(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'ogrn', 'inn', 'kpp', 'registration_date', 'phone', 'web')
    list_display_links = ('id', 'short_name', )
    search_fields = ('id', 'short_name', 'ogrn', 'inn', 'kpp', 'registration_date', 'phone', 'web')