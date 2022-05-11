from django.http import HttpResponseNotFound
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
from django_tables2 import RequestConfig

from apps.manage.filters import ReportFilter
from apps.manage.tables import ReportTable
from apps.project.models import Report
from apps.project.services import get_project_report


def report_list(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists():
        return HttpResponseNotFound("Страница не найдена")

    f = ReportFilter(request.GET, queryset=Report.objects.exclude(status=Report.DRAFT).all())

    context = {'filter': f}

    report_table = ReportTable(f.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(report_table)

    context['report_table'] = report_table

    return render(request, 'manage/report/report-list.html', context)


def report_view(request, project_id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists():
        return HttpResponseNotFound("Страница не найдена")

    report = get_project_report(project_id)
    context = {"report": report}

    return render(request, 'manage/report/report-view.html', context)


def report_change_status(request, project_id, status):
    if not request.user.is_authenticated:
        return redirect('account_login')

    if not request.user.groups.filter(name='admin').exists():
        return HttpResponseNotFound("Страница не найдена")

    report = get_project_report(project_id)

    if request.method == 'POST':
        report.status = status
        report.save()
        return redirect('manage-report-list')

    context = {"report": report, 'status': status }

    return render(request, 'manage/report/report-change-status.html', context)


