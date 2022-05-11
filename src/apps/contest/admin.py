from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .form import DocumentInlineForm
from .models import Direction, Subject, Contest, Coefficient, Criteria, ScoreSheet, Score, Document, DocumentTag, \
    Commission, ReportPeriod
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


class DocumentsInline(admin.TabularInline):
    model = Document
    form = DocumentInlineForm
    extra = 0


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'contest', 'file')
    form = DocumentInlineForm

    class Media:
        js = ('js/jquery/selectize.min.js', 'admin/js/contest.js')
        css = {'all': ('css/selectize.css',)}


@admin.register(DocumentTag)
class DocumentTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_hidden')


@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    """Конкурсы"""
    list_display = ('title', 'status')
    # list_editable = ("status",)
    list_filter = ('status',)
    search_fields = ['title']
    readonly_fields = ("author",)
    inlines = (DocumentsInline,)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    class Media:
        js = ('js/jquery/selectize.min.js', 'admin/js/contest.js')
        css = {'all': ('css/selectize.css',)}


class SubjectAdminInline(admin.TabularInline):
    extra = 0
    model = Subject


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    """Направления конкурсов"""
    inlines = (SubjectAdminInline,)
    list_display = ('title', 'max_sum', 'img')
    search_fields = ['title']
    list_display_links = ("title",)


@admin.register(Coefficient)
class CoefficientAdmin(admin.ModelAdmin):
    """Коэффициенты значимости"""
    list_display = ('contest', 'criteria', 'col500',
                    'col1000', 'col3000', 'colinf')
    list_editable = ('col500', 'col1000', 'col3000', 'colinf')
    search_fields = ['criteria']
    list_display_links = ("criteria",)
    list_filter = ('contest',)


@admin.register(Criteria)
class CriteriaAdmin(SummernoteModelAdmin):
    """Критерии оценки заявок на участие в конкурсе"""
    list_display = ('id', 'title',)
    search_fields = ['title']
    list_display_links = ("title",)
    summernote_fields = ('info',)


@admin.register(ReportPeriod)
class ReportPeriodAdmin(admin.ModelAdmin):
    """Сроки сдачи отчетности"""
    list_display = ('contest', 'date',)
    list_display_links = ("date",)
    list_filter = ('contest',)
    readonly_fields = ('notified', )


class ScoreAdminInline(admin.TabularInline):
    extra = 0
    fields = ('score', 'comment')
    can_delete = False
    model = Score


@admin.register(ScoreSheet)
class ScoreSheetAdmin(admin.ModelAdmin):
    """Оценочные листы"""
    inlines = (ScoreAdminInline,)
    # def score_sheet_url(self, obj):
    #    return format_html("<a href='/expert/edit-score-sheet/{project_id}'>test</a>", project_id=obj.project_id)

    # score_sheet_url.allow_tags = True
    # list_display_links = ("score_sheet_url",)
    list_display = ('contest', 'project_id', 'project', 'status', 'author', 'score_sum', 'score_total_sum')
    search_fields = ['project__id', 'project__title']
    list_display_links = ('author',)
    list_filter = (
        ('status', ChoiceDropdownFilter),
        'contest',
        'author',
    )


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    change_list_template = "admin/contest/score.html"
    """Оценки"""
    list_display = ('project_id', 'expert', 'criteria', 'score')

    def project_id(self, obj):
        return  obj.score_sheet.project_id
    project_id.short_description = '№ Заявки'

    def expert(self, obj):
        return  obj.score_sheet.author
    expert.short_description = 'Эксперт'

    list_editable = ('score',)
    search_fields = ['=score_sheet__project__id']
    list_display_links = ("criteria",)
    list_filter = (
        ('score_sheet__author', RelatedDropdownFilter),
        
    )


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('fio', 'order_field', 'position',)
    search_fields = ['fio']
    list_display_links = ("fio",)
