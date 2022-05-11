from django import forms

from .models import Document, DocumentTag


class DocumentInlineForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=DocumentTag.objects.all())

    class Meta:
        model = Document
        fields = '__all__'


