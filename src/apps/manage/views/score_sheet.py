from django.forms import modelformset_factory
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, get_object_or_404, render
from django import forms
from django_tables2 import RequestConfig
from django_tables2.export import TableExport

from apps.contest.models import ScoreSheet, Score
from apps.expert.forms import ScoreSheetForm
from apps.manage.filters import ScoreSheetFilter
from apps.manage.tables import ScoreSheetTable, ScoreSheetTableExcel


def score_sheet_list(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    f = ScoreSheetFilter(request.GET, queryset=ScoreSheet.objects.all())

    context = {'filter': f}

    score_sheet_table = ScoreSheetTable(f.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(score_sheet_table)

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        excel_table = ScoreSheetTableExcel(f.qs.order_by('project__id'))
        exporter = TableExport(export_format, excel_table)
        return exporter.response("score-sheet.xlsx")

    context['score_sheet_table'] = score_sheet_table

    return render(request, 'manage/score-sheet/score-sheet-list.html', context)


def edit_score_sheet(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    score_sheet = get_object_or_404(ScoreSheet, pk=id)
    ScoreFormset = modelformset_factory(
        Score, fields=('score', 'comment'),
        widgets={
            'score': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 1, 'onkeyup': 'enforceMinMax(this)'}),
            'comment': forms.Textarea(attrs={'cols': 40, 'rows': 2})
        },
        extra=0
    )

    if request.method == 'POST':
        formset = ScoreFormset(request.POST, queryset=Score.objects.filter(
            score_sheet_id=score_sheet.id))
        if formset.is_valid():
            formset.save()

        score_sheet_form = ScoreSheetForm(request.POST, instance=score_sheet)
        if score_sheet_form.is_valid:
            score_sheet_form.save()

    formset = ScoreFormset(queryset=Score.objects.filter(
        score_sheet_id=score_sheet.id))
    score_sheet_form = ScoreSheetForm(instance=score_sheet)
    context = {
        "score_sheet": score_sheet,
        "formset": formset,
        "score_sheet_form": score_sheet_form
    }

    return render(request, 'manage/score-sheet/edit-score-sheet.html', context)


def delete_score_sheet(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    score_sheet = get_object_or_404(ScoreSheet, pk=id)
    score_sheet.delete()

    return redirect('manage-score-sheet-list')
