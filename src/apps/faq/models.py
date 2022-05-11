from django.db import models
from django.contrib.auth.models import User


class Faq(models.Model):
    question = models.CharField(max_length=500, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question

    # @staticmethod
    # def get_list(limit):
    #     return News.objects.order_by('-created_on').all()[:limit]

