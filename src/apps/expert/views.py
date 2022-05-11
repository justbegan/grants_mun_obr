from django import forms
from django.forms import modelformset_factory
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django_tables2 import RequestConfig

from apps.contest.models import Score, ScoreSheet, Document
from apps.project.services import get_expert_projects, get_score_sheet, get_score_sheets
from apps.user.filters import ProjectFilter
from .forms import ScoreSheetForm
from .tables import ProjectTable, ScoreSheetTable
from ..manage.filters import ScoreSheetFilter


def index(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='expert').exists():
        return HttpResponseNotFound("Страница не найдена")

    f = ProjectFilter(request.GET, queryset=get_expert_projects(request.user.pk))

    context = {'filter': f }

    project_table = ProjectTable(f.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(project_table)

    context['project_table'] = project_table

    return render(request, 'expert/index.html', context)


def edit_score_sheet(request, project_id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='expert').exists():
        return HttpResponseNotFound("Страница не найдена")

    score_sheet = get_score_sheet(project_id, request.user.pk)

    if score_sheet.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    if score_sheet.status == score_sheet.FINISHED:
        return redirect('expert-view-score-sheet', score_sheet.id)

    ScoreFormset = modelformset_factory(
        Score, fields=('score', 'comment'), 
        widgets={
            'score': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step':1 , 'onkeyup': 'enforceMinMax(this)'}),
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
        if score_sheet_form.is_valid():
            score_sheet_form.save()

        if 'approve' in request.POST:
            score_sheet.status = score_sheet.FINISHED
            score_sheet.save()
            return redirect('expert-score-sheet-list')

    formset = ScoreFormset(queryset=Score.objects.filter(
        score_sheet_id=score_sheet.id))
    score_sheet_form = ScoreSheetForm(instance=score_sheet)

    context = {
        "score_sheet": score_sheet,
        "formset": formset,
        "score_sheet_form": score_sheet_form,
    }

    return render(request, 'expert/edit-score-sheet.html', context)


def finish_score_sheet(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='expert').exists():
        return HttpResponseNotFound("Страница не найдена")

    score_sheet = get_object_or_404(ScoreSheet, pk=id)

    if score_sheet.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    score_sheet.status = ScoreSheet.FINISHED
    score_sheet.save()

    return redirect('expert-score-sheet-list')


def view_score_sheet(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='expert').exists() and not request.user.groups.filter(name='admin').exists():
        return HttpResponseNotFound("Страница не найдена")

    score_sheet = get_object_or_404(ScoreSheet, pk=id)

    if score_sheet.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    context = {
        "score_sheet": score_sheet,
    }

    return render(request, 'expert/view-score-sheet.html', context)


def score_sheet_list(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='expert').exists():
        return HttpResponseNotFound("Страница не найдена")

    f = ScoreSheetFilter(request.GET, queryset=get_score_sheets(request.user.pk))

    context = {'filter': f}

    score_sheet_table = ScoreSheetTable(f.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(score_sheet_table)

    context['score_sheet_table'] = score_sheet_table

    return render(request, 'expert/score-sheet-list.html', context)


def delete_score_sheet(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='expert').exists():
        return HttpResponseNotFound("Страница не найдена")

    score_sheet = get_object_or_404(ScoreSheet, pk=id)
    if score_sheet.status == score_sheet.FINISHED:
        return redirect('expert-view-score-sheet', score_sheet.id)

    score_sheet.delete()

    return redirect('expert-score-sheet-list')


def documents(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='expert').exists():
        return HttpResponseNotFound("Страница не найдена")

    docs = Document.objects.filter(tags__slug='expert').all()


    return render(request, 'expert/documents.html', { 'docs': docs })
