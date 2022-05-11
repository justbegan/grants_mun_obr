import os
import datetime
import json

from django import forms
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.http import urlquote
from django_tables2 import RequestConfig
from rest_framework.parsers import JSONParser

from ..project.models.reporting import ReportingEvent, ReportingEventLink, ReportingIndicator, ReportingIndicatorLink, \
    ReportingExpense, AgreementFile, ReportingBest, ReportingBestFile

if not os.name == 'nt':
    from weasyprint import HTML
import array

from apps.contest.serializers import ContestSerializer
from apps.project.models import ProjectFile, Education, Regions, Project, GenericCost, Event
from apps.project.serializers import ProjectSerializer
from apps.project.services import create_empty_project, update_project, remove_project, get_score_sheet
from apps.project.services import get_user_projects, get_open_contest, get_project, get_project_report
from .filters import ProjectFilter
from .forms import DocumentForm, RequestFileForm
from .serializers import ReportSerializer, ReportEventSerializer
from .tables import ProjectTable, ReportTable
from ..contest.models import Score, Criteria, Coefficient
from ..expert.forms import ScoreSheetForm
from apps.project.services.checklist import OrganizationValidate
from apps.contur.models import Organization as OrganizationData


def index(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    f = ProjectFilter(request.GET, queryset=get_user_projects(request.user.pk))

    context = {'filter': f}

    project_table = ProjectTable(f.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(project_table)

    context['contest'] = get_open_contest()
    context['project_table'] = project_table

    return render(request, 'user/index.html', context)


def create_project(request, contest_id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    data = {
        "contest_id": contest_id,
        "user_id": request.user.id
    }

    project = create_empty_project(data)

    return redirect('user-edit-project', id=project.pk)


def view_project(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')
    project = get_project(id)
    experts_ids = []
    iam_expert_for_this_project = False
    for e in project.experts.all():
        experts_ids.append(e.id)
        if e.id == request.user.id:
            iam_expert_for_this_project = True

    if project.author_id != request.user.id \
            and not request.user.groups.filter(name='admin').exists() \
            and not iam_expert_for_this_project:
        return redirect('profile-home')

    formset = None
    score_sheet_form = None
    score_sheet = None

    if request.user.groups.filter(name='expert').exists():
        score_sheet = get_score_sheet(id, request.user.pk)
        ScoreFormset = modelformset_factory(
            Score, fields=('score', 'comment'),
            widgets={
                'score': forms.NumberInput(
                    attrs={'min': 0, 'max': 10, 'pattern': "[0-9]", 'step': 1, 'onkeyup': 'enforceMinMax(this)'}),
                'comment': forms.Textarea(attrs={'cols': 40, 'rows': 2})
            },
            extra=0
        )

    if request.method == 'POST':
        form = RequestFileForm(request.POST, request.FILES)
        if form.is_valid():
            project.request_file = request.FILES['file']
            project.save()

            return redirect('user-view-project', id)

        if request.user.groups.filter(name='expert').exists():
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

        elif request.user.groups.filter(name__in=['admin']).exists():
            org_data: OrganizationData = None
            if project.organization.ogrn:
                org_data = OrganizationData.objects.filter(ogrn=project.organization.ogrn).first()
            checklist = OrganizationValidate(project.organization, org_data).fromForm(request.POST)

            # Видимо раньше в полях были другие критерии, которые автоматом выставлялись в true и false
            # Отключил
            # checklist.autofillFromOrg()
            project.organization.checklist = checklist.toSaveJSON()
            project.organization.save()

    else:
        form = RequestFileForm()

    if request.user.groups.filter(name='expert').exists():
        formset = ScoreFormset(queryset=Score.objects.filter(
            score_sheet_id=score_sheet.id))
        score_sheet_form = ScoreSheetForm(instance=score_sheet)

    types = []
    for t in GenericCost.TYPE:
        types.append(t[0])

    project.organization.checklist = OrganizationValidate(project.organization, None).toJSON()

    context = {
        "ids": experts_ids,
        "id": iam_expert_for_this_project,
        "score_sheet": score_sheet,
        "formset": formset,
        "score_sheet_form": score_sheet_form,
        "budget_types": types,
        "budget_type": dict((t, name) for t, name in GenericCost.TYPE),

        "project": project,
        "csrf_token": get_token(request),
        "form": form
    }

    return render(request, 'user/view-project.html', context)


def view_expertise(request, project_id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    project = get_project(project_id)
    if project.author_id != request.user.id \
            or not request.user.groups.filter(name='admin').exists() \
            or not request.user.groups.filter(name='expert').exists():
        redirect('contest-home')

    coefficients = Coefficient.objects.filter(contest=project.contest).all()
    ac = []
    for c in coefficients:
        ac.append({'title': c.criteria.title, 'score': c.criteria.project_score(project_id)})

    context = {
        "project": project,
        "criteria": ac
    }

    return render(request, 'user/view-expertise.html', context)


def edit_project(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    project = get_project(id)

    if project.author != request.user:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    if project.status != project.DRAFT and project.status != project.FIX and request.user.username != 'bastaky':
        return redirect('user-view-project', id)

    contest = project.contest

    exclude_directions = []
    user_projects = get_user_projects(user_id=request.user.id)
    for p in user_projects:
        if p.direction and p.direction != project.direction:
            exclude_directions.append(p.direction.id)

    directions = contest.directions.exclude(id__in=exclude_directions)

    dict_directions = []
    for d in directions.all():
        subjects = []
        for s in d.subjects():
            subjects.append({
                "id": s.id,
                "title": s.title
            })
        dict_directions.append({
            "id": d.id,
            "title": d.title,
            "subjects": subjects
        })

    context = {
        "contest": ContestSerializer(contest).to_json(),
        "directions": json.dumps(dict_directions),
        "educations": json.dumps(Education.EDU),
        "project_id": id,
        "csrf_token": get_token(request),
        "project": ProjectSerializer(project).to_json()
    }
    if project.status == project.FIX:
        return render(request, 'user/fix-project.html', context)

    return render(request, 'user/edit-project.html', context)


def save_project(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')

    project = get_project(id)
    if project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return JsonResponse({'status': 'error'})

    if project.status != project.DRAFT and project.status != project.FIX and request.user.username != 'bastaky':
        return JsonResponse({'status': 'error'})

    json_string = request.body

    project = update_project(project, json.loads(json_string))

    return JsonResponse({'status': 'ok', 'project': ProjectSerializer(project).to_json()})


def report_list(request):
    if not request.user.is_authenticated:
        return redirect('login')

    f = ProjectFilter(request.GET, queryset=get_user_projects(request.user.pk).filter(status=Project.WIN))

    context = {'filter': f}

    report_table = ReportTable(f.qs)
    RequestConfig(request, paginate={"per_page": 10}).configure(report_table)

    context['contest'] = get_open_contest()
    context['report_table'] = report_table

    return render(request, 'user/report-list.html', context)


def report_project(request, project_id):
    if not request.user.is_authenticated:
        return redirect('login')

    project = get_project(project_id)
    if project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    report = get_project_report(project_id)
    report_serializer = ReportSerializer(report)
    report_dict = report_serializer.data
    if not 'grant_sum' in report_dict['cost']:
        report_dict['cost']['grant_sum'] = str(project.budget_request_sum())

    events = []
    for event in project.event_set.all():
        event_serializer = ReportEventSerializer(event)
        events.append(event_serializer.data)

    context = {
        "project": project,
        'report': json.dumps(report_serializer.data),
        'events': json.dumps(events),
        "project_id": project_id,
        "csrf_token": get_token(request),
    }

    return render(request, 'user/report-project.html', context)


def save_report(request, project_id):
    if not request.user.is_authenticated:
        return redirect('login')

    report = get_project_report(project_id)
    project = get_project(project_id)

    if project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    data = JSONParser().parse(request)
    report_serializer = ReportSerializer(report, data=data['report'])

    event_serializers = []
    for event in data['events']:
        e = Event.objects.get(pk=int(event['id']))
        event_serializer = ReportEventSerializer(e, data=event)
        event_serializers.append(event_serializer)
        if event_serializer.is_valid():
            event_serializer.save()
        else:
            return JsonResponse(event_serializer.errors, status=400)

    if report_serializer.is_valid():
        report_serializer.save()
        return JsonResponse({
            'report': report_serializer.data,
        }, status=201)

    return JsonResponse(report_serializer.errors, status=400)


def publish_report(request, project_id):
    if not request.user.is_authenticated:
        return redirect('account_login')
    report = get_project_report(project_id)
    project = get_project(project_id)

    if project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    if report.status == report.DRAFT or report.status == report.FIX:
        report.status = report.NEW
        report.save()

    return redirect('user-report-list')


def regions(request, query=None):
    if not request.user.is_authenticated:
        return redirect('login')

    query = request.GET.get('q', query)
    filtered_dict = Regions.get_filtered(query) if query else Regions.get_all()

    return HttpResponse(json.dumps(filtered_dict, ensure_ascii=False), content_type="application/json")


def fill_fields(request, project_id):
    if not request.user.is_authenticated:
        return redirect('account_login')
    project = get_project(project_id)

    if project.author_id != request.user.id:
        return redirect('contest-home')

    context = {
        'project': project
    }
    return render(request, 'user/fill-fields.html', context)


def direction_max_sum(request, project_id):
    if not request.user.is_authenticated:
        return redirect('account_login')
    project = get_project(project_id)

    if project.author_id != request.user.id:
        return redirect('contest-home')

    context = {
        'project': project
    }
    return render(request, 'user/direction-max-sum.html', context)


def publish_project(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')
    project = get_project(id)
    if project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    if project.direction:
        if project.direction.max_sum and project.direction.max_sum > 0:
            if project.budget_request_sum() > project.direction.max_sum:
                return redirect('user-direction-max-sum', id)

    if project.about_percent() < 100 or project.manager_percent() < 100 \
            or project.members_percent() < 100 or project.organization_percent() < 100 \
            or project.cost_count_num() < 1 or project.events_count_num() < 1:
        return redirect('user-fill-fields', id)

    if project.status == project.DRAFT or project.status == project.FIX:
        if project.status == project.DRAFT:
            project.request_date = datetime.datetime.now()
        project.status = project.NEW
        project.save()

    return redirect('user-view-project', id)


def delete_project(request, id):
    if not request.user.is_authenticated:
        return redirect('account_login')
    project = get_project(id)
    if project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    remove_project(project)

    return redirect('user-home')


def upload_file(request, type, project_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false', 'message': 'access denied'}, status=403)

    project = get_project(project_id)
    if project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = ProjectFile(
                project_id=project_id, file=request.FILES['file'], type=type)
            newdoc.save()
            project.save()

            return JsonResponse({
                'status': 'ok',
                'file': {
                    'id': newdoc.id,
                    'name': newdoc.file.name,
                    'type': newdoc.type
                }
            })

        return JsonResponse({'status': 'false', 'message': form.errors}, status=500)
    else:
        return JsonResponse({'status': 'false', 'message': 'invalid request method'}, status=500)


def delete_file(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false', 'message': 'access denied'}, status=403)

    file = get_object_or_404(ProjectFile, pk=id)
    if file.project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    is_standart = str.startswith(file.file.url, '/media/contur/') or str.startswith(file.file.url, '/contur/')
    if is_standart:
        file.project.projectfile_set.all().filter(id=id).delete()

    else:
        file.delete()
        file.project.save()

    return JsonResponse({'status': 'ok'})


def request_pdf(request, project_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'false', 'message': 'access denied'}, status=403)

    project = get_project(project_id)
    if project.author_id != request.user.id:
        if not request.user.groups.filter(name='admin').exists():
            return redirect('contest-home')

    response = HttpResponse(content_type="application/pdf")
    response['Content-Disposition'] = "inline; filename=request.pdf"
    html = render_to_string("user/request-pdf.html", {
        'project': project,
        'user': request.user
    })

    HTML(string=html).write_pdf(response)
    return response


@login_required
def agreements_project(request, id):
    project = get_project(id)
    u = request.user
    is_admin = u.groups.filter(name='admin').exists()
    if project.author_id != u.id \
            or not is_admin \
            or not u.groups.filter(name='expert').exists():
        redirect('contest-home')

    if is_admin and request.method == 'POST':
        post = request.POST
        if post.get('type') == 'srok':
            project.report_date = datetime.datetime.strptime(post.get('srok'), '%d.%m.%Y').strftime('%Y-%m-%d')
            project.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '#results')
        elif post.get('type') == 'main':
            for a in project.agreementfile_set.all():
                if a.type == AgreementFile.TYPE_AGREEMENT:
                    a.delete()
            t = AgreementFile.TYPE_AGREEMENT
        elif post.get('type') == 'results':
            t = AgreementFile.TYPE_CHECK_RESULTS
        else:
            t = AgreementFile.TYPE_ADDITIONAL_AGREEMENT
        d = datetime.datetime.strptime(post.get('date'), '%d.%m.%Y').strftime('%Y-%m-%d')
        a = AgreementFile(title=post.get('title'), number=post.get('number'), date=d, file=request.FILES.get('file'),
                          project=project, type=t)
        a.save()
        # return HttpResponseRedirect(request.path_info)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + '#results')

    context = {
        "project": project,
        'is_admin_form': is_admin
    }

    return render(request, 'user/agreements-project.html', context)


@login_required
def reporting_project(request, id):
    project = get_project(id)
    u = request.user
    if project.author_id != u.id \
            or not u.groups.filter(name='admin').exists() \
            or not u.groups.filter(name='expert').exists():
        redirect('contest-home')

    if request.method == 'POST':
        t = request.POST.get('type')
        if t == 'events':
            es = json.loads(request.POST.get('events_json'))
            for e in es:
                if e['id']:
                    re = ReportingEvent.objects.get(id=e['id'])
                    re.name = e['name']
                    re.start_date = e['start_date']
                    re.finish_date = e['finish_date']
                    if re.name:
                        re.save()
                    else:
                        re.delete()
                else:
                    m = ReportingEvent(**e)
                    m.project = project
                    m.save()
        elif t == 'events_fulfillment':
            es = json.loads(request.POST.get('events_json'))
            for e in es:
                re = ReportingEvent.objects.get(id=e['id'])
                re.fulfillment = e['fulfillment']
                re.save()
        elif t == 'links':
            entity_type = request.POST.get('entityType')
            if entity_type == 'plan':
                model = ReportingEvent
                model2 = ReportingEventLink
                z_s = 'reporting_event'
            elif entity_type == 'achievement':
                model = ReportingIndicator
                model2 = ReportingIndicatorLink
                z_s = 'indicator'
            re = model.objects.get(id=request.POST.get('entityId'))
            ls = json.loads(request.POST.get('links_json'))
            for l in ls:
                if l['id']:
                    link = model2.objects.get(id=l['id'])
                    link.url = l['url']
                    if link.url:
                        link.save()
                    else:
                        link.delete()
                else:
                    m = model2(**l)
                    setattr(m, z_s, re)
                    m.save()
        elif t == 'file':
            z = {}
            if 'event' in request.POST:
                model = ReportingEvent
                id = request.POST.get('event')
                z_s = 'reporting_event'
            elif 'indicator' in request.POST:
                model = ReportingIndicator
                id = request.POST.get('indicator')
                z_s = 'indicator'
            elif 'expense' in request.POST:
                model = ReportingExpense
                id = request.POST.get('expense')
                z_s = 'expense'
            t = request.POST.get('file_type')
            re = model.objects.get(id=id)
            z[z_s] = re
            for f in request.FILES.getlist('file'):
                if model == ReportingExpense:
                    re.files.create(file=f, **z)
                else:
                    re.files.create(file=f, type=t, **z)
            if not request.is_ajax():
                return HttpResponseRedirect(request.path_info)
        elif t == 'file-delete':
            if 'event' in request.POST:
                model = ReportingEvent
                id = request.POST.get('event')
            elif 'indicator' in request.POST:
                model = ReportingIndicator
                id = request.POST.get('indicator')
            elif 'expense' in request.POST:
                model = ReportingExpense
                id = request.POST.get('expense')
            re = model.objects.get(id=id)
            re.files.get(id=request.POST.get('file')).delete()
        elif t == 'field-delete':
            if 'event' in request.POST:
                model = ReportingEvent
                id = request.POST.get('event')
            elif 'expense' in request.POST:
                model = ReportingExpense
                id = request.POST.get('expense')
            re = model.objects.get(id=id)
            re.delete()
        elif t == 'indicators':
            is_user = request.POST.get('isUser') == 'true'
            i_s = json.loads(request.POST.get('indicators_json'))
            for i in i_s:
                if i['id']:
                    re = ReportingIndicator.objects.get(id=i['id'])
                    if is_user:
                        re.value = i['value']
                        re.reason = i['reason']
                    else:
                        re.date = i['date']
                        re.planned = i['planned']
                    re.save()
                else:
                    m = ReportingIndicator(**i)
                    m.project = project
                    m.save()
        elif t == 'indicators_user':
            i_s = json.loads(request.POST.get('indicators_json'))
            for i in i_s:
                re = ReportingIndicator.objects.get(id=i['id'])
                re.value = i['value']
                re.reason = i['reason']
                re.save()
        elif t == 'costs':
            is_user = request.POST.get('isUser') == 'true'
            i_s = json.loads(request.POST.get('costs_json'))
            for i in i_s:
                if i['id']:
                    re = ReportingExpense.objects.get(id=i['id'])
                    if is_user:
                        re.value = i['value']
                        re.save()
                    else:
                        re.name = i['name']
                        if re.name:
                            re.qty = i['qty']
                            re.unit_cost = i['unit_cost']
                            re.overall = i['overall']
                            re.planned = i['planned']
                            re.save()
                        else:
                            re.delete()
                else:
                    m = ReportingExpense(**i)
                    m.project = project
                    m.save()
        elif t == 'best':
            best_data = json.loads(request.POST.get('best_json'))
            if len(project.bests.all()) == 0:
                best = ReportingBest()
                best.project = project
            else:
                best = project.bests.all()[0]

            best.description = best_data['description']
            best.beneficiaries_count = best_data['beneficiaries_count']
            best.volunteers_count = best_data['volunteers_count']
            best.self_co_financing = best_data['self_co_financing']
            best.targets = best_data['targets']
            best.additional_amount = best_data['additional_amount']
            best.links = best_data['links']
            best.save()

        elif t == 'pdf':
            context = {
                "project": project,
            }
            response = HttpResponse(content_type="application/pdf")
            response['Content-Disposition'] = "inline; filename=project.pdf"
            html = render_to_string("user/reporting-project/pdf.html", context)
            HTML(string=html).write_pdf(response)
            return response
        return HttpResponse('1')

    # report_status_change
    # Изменение report_status из user/reporting-project/<int:id>
    # url reporting-project/<int:pk>/rep_status
    if request.is_ajax():
        problem_obj = Project.objects.get(id=id)
        problem_obj.report_status = request.GET['input_status']
        problem_obj.save()
        return JsonResponse({'status': 200})

    if request.GET.get('task') == 'pdf':
        t = request.GET.get('type')
        context = {
            "project": project,
            'landscape': t != 'plan'
        }
        if t == 'plan':
            filename = 'Отчет по исполнению Календарного плана'
        if t == 'achievement':
            filename = 'Отчет о достижении показателей'
            context['indicator_types'] = ReportingIndicator.TYPES
            context['indicators'] = ReportingIndicator.get_for_project(project)
        if t == 'costs':
            filename = 'Отчет о расходах'
            context['expense_types'] = ReportingExpense.TYPES
            context['expenses'] = ReportingExpense.get_for_project(project)
        response = HttpResponse(content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename*=UTF-8\'\'{}'.format(urlquote(filename + '.pdf'))
        html = render_to_string("user/reporting-project/pdf-" + t + ".html", context)
        HTML(string=html).write_pdf(response)
        return response

    e_j = []
    for e in project.event_set.all():
        e_j.append({
            'name': e.name,
            'start': e.start_date.strftime('%d.%m.%Y'),
            'end': e.finish_date.strftime('%d.%m.%Y')
        })
    context = {
        "project": project,
        'best': project.bests.all()[0] if len(project.bests.all()) > 0 else ReportingBest(),
        'is_user_form': project.author_id == u.id,
        'is_admin_form': u.groups.filter(name='admin').exists(),
        'events_json': json.dumps(e_j),
        'indicator_types': ReportingIndicator.TYPES,
        'indicators': ReportingIndicator.get_for_project(project),
        'expense_types': ReportingExpense.TYPES,
        'expenses': ReportingExpense.get_for_project(project)
    }

    return render(request, 'user/reporting-project.html', context)
