from django.contrib import admin

from .models import Faq


class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_on', 'author')
    search_fields = ['question', 'answer']
    readonly_fields = ('created_on', 'author')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user

        super(FaqAdmin, self).save_model(request, obj, form, change)


admin.site.register(Faq, FaqAdmin)

