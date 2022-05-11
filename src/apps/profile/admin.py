from django import forms
from django.contrib import admin

from .models import Profile
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

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ('user', )
    search_fields = ('user__username', 'user__email', 'mobile_phone', 'phone')
    list_display = ('user_info', 'mobile_phone', 'phone')
    filter_horizontal = ('directions',)
    form = ProfileForm

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('user')

    def user_info(self, obj):
        return obj.user.username + ' ' + obj.user.email


