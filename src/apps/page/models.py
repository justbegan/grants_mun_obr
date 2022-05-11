from django.db import models

from ..contest.models import DocumentTag


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=160, unique=True, verbose_name="ЧПУ")
    html = models.TextField(verbose_name='HTML')
    related_tag = models.ForeignKey(DocumentTag, on_delete=models.DO_NOTHING, blank=True, null=True,
                                    verbose_name='Связанный тэг документов')

    class Meta:
        ordering = ['title']
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'

    def __str__(self):
        return self.title


