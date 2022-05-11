from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    img = models.ImageField(upload_to='course', verbose_name='Картинка', blank=False)
    html = models.TextField(verbose_name='HTML')
    # TODO type? lessons? wtf, how is this supposed to work
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Онлайн-курс'
        verbose_name_plural = 'Онлайн-курсы'

    def __str__(self):
        return self.title

    # @staticmethod
    # def get_list(limit):
    #     return News.objects.order_by('-created_on').all()[:limit]

