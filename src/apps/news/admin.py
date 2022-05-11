from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .functions import make_thumb, add_prefix_to_file_name
from .models import News


class NewsAdmin(SummernoteModelAdmin):
    list_display = ('title', 'created_on', 'author')
    search_fields = ['title', 'content']
    readonly_fields = ('author', 'thumb')
    summernote_fields = ('content',)

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user

        super(NewsAdmin, self).save_model(request, obj, form, change)

        if 'img' in form.changed_data:
            if obj.img and make_thumb(obj.img.path, (News.THUMB_WIDTH, News.THUMB_HEIGHT)):
                obj.thumb = add_prefix_to_file_name(obj.img.url, News.THUMB_PREFIX)
            else:
                obj.thumb = None
            obj.save(update_fields=('thumb', ))


admin.site.register(News, NewsAdmin)

