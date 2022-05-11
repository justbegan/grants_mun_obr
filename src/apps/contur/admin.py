from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Организации"""
    list_display = ('id', 'short_name', 'ogrn')
    search_fields = ['short_name', 'id', 'ogrn', 'inn']
    list_display_links = ('id', "short_name",)