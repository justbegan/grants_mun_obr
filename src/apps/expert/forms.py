from django import forms

from apps.contest.models import ScoreSheet


class ScoreForm(forms.Form):
    score = forms.DecimalField()
    comment = forms.CharField(widget=forms.CheckboxInput())


class ScoreSheetForm(forms.ModelForm):

    class Meta:
        model = ScoreSheet
        fields = ('additional_score1', 'additional_score2','result')
        labels = {
            'additional_score1': '',
        }
        widgets = {
            'additional_score1': forms.NumberInput(
                attrs={'min': 0, 'max': 5, 'step': 1, 'onkeyup': 'enforceMinMax(this)'}),
            'additional_score2': forms.NumberInput(
                attrs={'min': 0, 'max': 5, 'step': 1, 'onkeyup': 'enforceMinMax(this)'}),
        }
