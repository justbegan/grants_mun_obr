import os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required


from apps.project.models import Organization
from apps.contur.models import Organization as Org
from django.template.loader import render_to_string
if not os.name == 'nt':
    from weasyprint import HTML

# from .filters import ProjectFilter
from .services.conturapi import RequesOrg

@login_required
def index(request):
    # f = ProjectFilter(request.GET, queryset=Project.objects.exclude(status=Project.DRAFT))

    organizations = Organization.objects.exclude(inn=None).exclude(inn='')[:10]

    context = {
        'title': '1',
        'organizations': organizations
    }

    return render(request, 'contur/index.html', context)

@login_required
def api_req(request):

    ogrn = request.GET.get('ogrn')

    org = get(ogrn, True)

    data = {
        'org': org
    }
    return JsonResponse(data)


# если изменили код и хотите обновить существующие = измените это
REQUEST_VER = 'v1-1'

def get(ogrn, force = False):
    org = None
    data = None

    # обновить данные при изменении кода
    ver_diff = True

    if not force:
        org = Org.objects.filter(ogrn=ogrn).first()
        if org:
            ver_diff = org.request_ver == REQUEST_VER


    if not org or force or not ver_diff:
        org = RequesOrg(ogrn, request_ver=REQUEST_VER)

    if org:
        data = org.basic[0]
        data['short_name'] = org.short_name
        data['full_name'] = org.full_name
        data['analytics'] = org.analytics[0]
        data['ergDetails'] = org.egr_details[0]

        data['file_egr'] = org.file_egr.url if org.file_egr else None

    return data