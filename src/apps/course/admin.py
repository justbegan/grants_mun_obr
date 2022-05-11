from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'author')
    search_fields = ('title', )
    readonly_fields = ('created_on', 'author')

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user

        super(CourseAdmin, self).save_model(request, obj, form, change)


admin.site.register(Course, CourseAdmin)

