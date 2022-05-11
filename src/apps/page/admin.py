from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Page


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ['title', 'html']
    summernote_fields = ('html',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'related_tag' in form.base_fields:
            form.base_fields['related_tag'].widget.can_add_related = False
            form.base_fields['related_tag'].widget.can_delete_related = False
            form.base_fields['related_tag'].widget.can_change_related = False
        return form

