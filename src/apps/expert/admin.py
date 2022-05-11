from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.html import format_html

from .models import Expert, Applicant
from ..profile.models import Profile
from ..project.services import get_open_contest


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        dirs = get_open_contest().directions.all();
        w = self.fields['directions'].widget
        choices = []
        for choice in dirs:
            choices.append((choice.id, choice.title))
        w.choices = choices

class ExpertProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    # verbose_name_plural = 'Profile'
    # fk_name = 'user'
    form = ProfileForm
    filter_horizontal = ('directions',)


@admin.register(Expert)
class ExpertAdmin(UserAdmin):
    list_display = ('username', 'is_active', 'user_name', 'org_name', 'email', 'phone', 'directions')
    search_fields = ('username', 'last_name', 'first_name', 'email',
                     'profile__middle_name', 'profile__mobile_phone', 'profile__phone',
                     'profile__organization', 'profile__locality',)
    inlines = (ExpertProfileInline, )
    list_filter = ()

    def user_name(self, obj):
        return obj.last_name + ' ' + obj.first_name + ' ' + obj.profile.middle_name
    user_name.short_description = 'Имя'

    def is_active(self, obj):
        return obj.is_active
    is_active.short_description = 'Активный'

    def org_name(self, obj):
        return obj.profile.organization
    org_name.short_description = 'Организация'

    def phone(self, obj):
        return obj.profile.phone
    phone.short_description = 'Контактный телефон'

    def locality(self, obj):
        return obj.profile.locality
    locality.short_description = 'Населенный пункт'

    def directions(self, obj):
        sd = "<ol>"
        for d in obj.profile.directions.all():
            sd = sd + '<li>' + d.title + '</li>'
        sd = sd + "</ol>"
        return format_html(sd)
    directions.short_description = 'Направления'



    def get_queryset(self, request):
        return User.objects.filter(groups__name=Expert.EXPERT_GROUP).prefetch_related('profile')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    # def has_change_permission(self, request, obj=None):
    #     return False

    class Media:
        css = {
            'all': ('admin/css/directions.css',)
        }

@admin.register(Applicant)
class ApplicantAdmin(UserAdmin):
    list_display = ('username', 'user_name', 'org_name', 'email', 'phone', 'locality')
    search_fields = ('username', 'last_name', 'first_name', 'email',
                     'profile__middle_name', 'profile__mobile_phone', 'profile__phone',
                     'profile__organization', 'profile__locality',)
    inlines = (ExpertProfileInline, )
    list_filter = ()

    def user_name(self, obj):
        return obj.last_name + ' ' + obj.first_name
    user_name.short_description = 'Имя'

    def org_name(self, obj):
        return obj.profile.organization
    org_name.short_description = 'Организация'

    def phone(self, obj):
        return obj.profile.phone
    phone.short_description = 'Контактный телефон'

    def locality(self, obj):
        return obj.profile.locality
    locality.short_description = 'Населенный пункт'

    def get_queryset(self, request):
        return User.objects.annotate(page_count=Count('project')).filter(page_count__gte=1)

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False



