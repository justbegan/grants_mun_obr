from django import forms
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    if not value.name.endswith('.pdf') and not value.name.endswith('.PDF'):
        raise ValidationError('Загружать можно только pdf файлы')

def validate_file_size(value):
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Файл слишком большой. Размер файла не должен превышать 10 мегабайт.')

class DocumentForm(forms.Form):
    file = forms.FileField(
        label='Выберите файл',
        help_text=''
    )


class RequestFileForm(forms.Form):
    file = forms.FileField(
        label='Добавить подписанный скан подтверждения подачи заявки',
        help_text='Документ должен быть загружен одним файлом в формате PDF, объемом не более 10 мегабайт.',
        validators=[validate_file_extension, validate_file_size]
    )

