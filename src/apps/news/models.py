from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    THUMB_WIDTH = 260
    THUMB_HEIGHT = 800  # make width prevail
    THUMB_PREFIX = 'thumb_'

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Текст новости")
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(verbose_name="Дата")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    img = models.ImageField(upload_to='news/%Y/%m/%d', verbose_name='Картинка', default=None, blank=True, null=True)
    thumb = models.TextField(default=None, null=True, max_length=400, verbose_name="Картинка")
    for_munobr = models.BooleanField(default=False,verbose_name="Для мун. обр")
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title

    @staticmethod
    def get_list(limit):
        print(News.objects.order_by('-created_on').all()[:limit])
        return News.objects.order_by('-created_on').all()[:limit]


