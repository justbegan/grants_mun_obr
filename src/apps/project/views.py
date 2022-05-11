import os
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.db.models import Q
from notifications.signals import notify

from apps.project.models import Project, GenericCost
from django.template.loader import render_to_string

from .services.notify import send_email_async

if not os.name == 'nt':
    from weasyprint import HTML

from .filters import ProjectFilter


def index(request):
    f = ProjectFilter(request.GET, queryset=Project.objects.exclude(status=Project.DRAFT))

    context = {'filter': f}

    current_page = Paginator(f.qs, 20)
    page = request.GET.get('page')
    try:
        # Если существует, то выбираем эту страницу
        context['projects'] = current_page.page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        context['projects'] = current_page.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        context['projects'] = current_page.page(current_page.num_pages)

    return render(request, 'project/index.html', context)


def view(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(request, 'project/view.html', {'project': project})


def vote(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    return render(request, 'project/vote.html', {'project': project})


def user_vote(request, project_id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    project = get_object_or_404(Project, pk=project_id)
    voted = False
    if project.votes.exists(request.user.id):
        voted = True
    else:
        project.votes.up(request.user.id)

    return render(request, 'project/user-vote.html', {'project': project, 'voted': voted})


def vote_projects(request):
    f = ProjectFilter(request.GET, queryset=Project.objects.filter(status=Project.WIN).all())

    context = {'filter': f}

    current_page = Paginator(f.qs, 20)
    page = request.GET.get('page')
    try:
        # Если существует, то выбираем эту страницу
        context['projects'] = current_page.page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        context['projects'] = current_page.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        context['projects'] = current_page.page(current_page.num_pages)

    return render(request, 'project/vote-projects.html', context)


def best_projects(request):
    f = ProjectFilter(request.GET, queryset=Project.objects.filter(best=True).all())

    context = {'filter': f}

    current_page = Paginator(f.qs, 20)
    page = request.GET.get('page')
    try:
        # Если существует, то выбираем эту страницу
        context['projects'] = current_page.page(page)
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        context['projects'] = current_page.page(1)
    except EmptyPage:
        # Если вышли за последнюю страницу, то возвращаем последнюю
        context['projects'] = current_page.page(current_page.num_pages)

    return render(request, 'project/best-projects.html', context)


def project_pdf(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    types = []
    for t in GenericCost.TYPE:
        types.append(t[0])

    context = {
        'project': project,
        "budget_types": types,
        "budget_type": dict((t, name) for t, name in GenericCost.TYPE),
    }
    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=project.pdf"
    html = render_to_string("project/pdf.html", context)
    HTML(string=html).write_pdf(response)
    return response


def cron(request):
    if request.GET.get('k') == '111122':
        now = datetime.datetime.now()
        # s = str(now)
        # f = open("cron.log", "a")
        # f.write(s + "\n\n")
        # f.close()
        if True:
            # сообщение победителям за месяц
            text = 'Министерство по делам молодежи и социальным коммуникациям Республики Саха (Якутия) ' \
                   'сообщает о необходимости сдачи отчетности по итогам реализации проекта на средства гранта ' \
                   'Главы Республики Саха (Якутия) на развитие гражданского общества'
            from apps.contest.models import Contest, ReportPeriod
            border = datetime.date.today() + datetime.timedelta(days=30)
            periods = ReportPeriod.objects.filter(notified=False, date__lte=border).all()
            for period in periods:
                contest = period.contest
                if contest.status != Contest.CLOSED:
                    projects = Project.objects.filter(contest=contest, status=Project.WIN).all()
                    for project in projects:
                        if True:
                            notify.send(project, recipient=project.author, verb=text)
                            send_email_async(project.title, text, [project.author.email])
                period.notified = True
                period.save()
        if True:
            # сообщение при не сдаче отчетности в срок
            projects = Project.objects.filter(status=Project.WIN, report_status=Project.REPORT_REALIZATION).all()
            for project in projects:
                #border = project.report_date if project.report_date else project.contest.reportperiod.date
                border = None
                if project.report_date:
                    border = project.report_date
                else:
                    if project.contest.reportperiod:
                        border = project.contest.reportperiod.date
                if border:
                    border = border + datetime.timedelta(days=1)
                    if border == datetime.date.today():
                        project.report_status = Project.REPORT_EXPIRE
                        project.save()
                        text = 'Статус отчетности изменен на: ' + project.report_status_name()
                        notify.send(project, recipient=project.author, verb=text)
                        send_email_async(project.title, text, [project.author.email])

    return HttpResponse('1')


def test(request):
    u = request.user
    project = Project.objects.get(id=2336)
    text = 'Министерство по делам молодежи и социальным коммуникациям Респу111'
    notify.send(project, recipient=u, verb=text)
    send_email_async(project.title, text, [project.author.email])
    return HttpResponse('1-2-3')


