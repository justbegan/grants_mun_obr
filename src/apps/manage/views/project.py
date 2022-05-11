from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport

from apps.manage.forms import AssignExpertsForm, CommentForm
from apps.manage.tables import ProjectTable, ProjectTableExcel, ReportingTable
from apps.project.models import Project, Comment
from apps.user.filters import ProjectFilter

from . import export as my_export
from ...contest.models import ScoreSheet
from ...project.services.notify import send_notify


def project_list(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    project_finished = request.GET.get('project_finished', False)
    qs = Project.objects.exclude(status='draft').all()

    """
    Проекты у которых все экспертизы завершены
    У проекта должны обязательно две экспертизы (оценочных листа)
    """
    if project_finished:
        qs = qs.annotate(scoresheet_count=Count('scoresheet')).filter(scoresheet_count__exact=2)
        qs = qs.exclude(scoresheet__status=ScoreSheet.NEW)

    f = ProjectFilter(request.GET, queryset=qs)

    context = {'filter': f}

    project_table = ProjectTable(f.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(project_table)

    export_form = request.GET.get("export_form", None)
    if export_form:
        if export_form == 'form1':
            return my_export.export_form1(request, f.qs)
        elif export_form == 'form2':
            return my_export.export_form2(request, f.qs)
        elif export_form == 'form3':
            return my_export.export_form3(request, f.qs)
        elif export_form == 'form4':
            return my_export.export_form4(request, f.qs)
        else:
            return HttpResponseNotFound("Форма экспорта не найдена")

    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        excel_table = ProjectTableExcel(f.qs)
        RequestConfig(request).configure(excel_table)
        exporter = TableExport(export_format, excel_table)
        return exporter.response("projects.xlsx")

    context['project_table'] = project_table
    context['project_finished'] = project_finished
    context['projects_count'] = f.qs.count()

    return render(request, 'manage/project/project-list.html', context)


def assign_experts(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    project = get_object_or_404(Project, pk=id)

    current_experts = []
    for expert in project.experts.all():
        current_experts.append(expert.id)
        
    if request.method == 'POST':
        form = AssignExpertsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            project = get_object_or_404(Project, pk=id)
            project.status = Project.ON_EXAM
            project.save()

            if project.status != project.ON_EXAM:
                send_notify(request.user, project.author, 'Заявка на экспертизе', project)
            send_notify(request.user, project.experts.exclude(id__in=current_experts).all(), 'Вам назначена заявка на экспертизу', project)

            return redirect('manage-home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        form = AssignExpertsForm(instance=project)

    return render(request, 'manage/project/assign-experts.html', {
        'project': project,
        'form': form,
    })


def project_to_fix(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    project = get_object_or_404(Project, pk=id)

    return change_project_status(request, project, Project.FIX, 'manage/project/to-fix.html', 'Заявка отправлена на доработку')


def project_to_check(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    project = get_object_or_404(Project, pk=id)

    return change_project_status(request, project, Project.ON_CHECK, 'manage/project/to-check.html', 'Заявка отправлена на проверку')


def project_win(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists():
        return HttpResponseNotFound("Страница не найдена")

    project = get_object_or_404(Project, pk=id)

    return change_project_status(request, project, Project.WIN, 'manage/project/win.html', 'Ваш проект получил поддержку')


def project_not_win(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    project = get_object_or_404(Project, pk=id)

    return change_project_status(request, project, Project.NOT_WIN, 'manage/project/not-win.html', 'Ваш проект не получил поддержку')


def project_reject(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    project = get_object_or_404(Project, pk=id)

    return change_project_status(request, project, Project.REJECT, 'manage/project/reject.html', 'Заявка отклонена')


def change_project_status(request, project, status, template, message = None):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    if request.method == 'POST':
        form = CommentForm(data=request.POST)

        new_comment = form.save(commit=False)
        new_comment.project = project
        new_comment.author = request.user
        new_comment.type = Comment.TYPE_INTERNAL
        if new_comment.content:
            new_comment.save()
        project.status = status
        project.save()

        if message:
            send_notify(request.user, project.author, message, project)

        return redirect('manage-home')

    else:
        form = CommentForm()

    return render(request, template, {
        'project': project,
        'form': form,
    })


@login_required
def reporting_list(request):
    if not request.user.groups.filter(name='admin').exists() and not request.user.groups.filter(name='admin2').exists():
        return HttpResponseNotFound("Страница не найдена")

    f = ProjectFilter(request.GET, queryset=Project.objects.exclude(status=Project.DRAFT).all())

    context = {'filter': f}

    project_table = ReportingTable(f.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(project_table)

    # export_format = request.GET.get("_export", None)
    # if TableExport.is_valid_format(export_format):
    #     excel_table = ProjectTableExcel(f.qs)
    #     exporter = TableExport(export_format, excel_table)
    #     return exporter.response("table.xlsx")

    context['project_table'] = project_table

    return render(request, 'manage/project/reporting-list.html', context)


