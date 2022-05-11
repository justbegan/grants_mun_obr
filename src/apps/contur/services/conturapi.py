import os
import datetime
from django.core import serializers
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import json

from apps.contur.models import Organization
import requests 

KONTUR_API_KEY = os.environ.get("KONTUR_API_KEY", ""),

def RequesOrg(ogrn, request_ver = ''):

    key = KONTUR_API_KEY[0]

    url = f'https://focus-api.kontur.ru/api3/req?ogrn={ogrn}&key={key}'
    url_ergDetails = f'https://focus-api.kontur.ru/api3/egrDetails?ogrn={ogrn}&key={key}'
    url_analytics = f'https://focus-api.kontur.ru/api3/analytics?ogrn={ogrn}&key={key}'

    url_excerpt = f'https://focus-api.kontur.ru/api3/excerpt?ogrn={ogrn}&key={key}'

    # if settings.DEBUG:
    #     url = 'http://localhost:2880/contur'
    #     url_ergDetails = 'http://localhost:2880/contur_detail'
    #     url_analytics = 'http://localhost:2880/contur_analytics'

    data = None
    z = None

    org = Organization.objects.filter(ogrn=ogrn).first()
    if not org: 
        org = Organization()

    try:
        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        if not data: return None

        ergDetails = requests.get(url_ergDetails)
        ergDetails.raise_for_status()
        data_ergDetails = ergDetails.json()


        analytics = requests.get(url_analytics)
        analytics.raise_for_status()
        data_analytics = analytics.json()

        upload_to='contur/%s' % datetime.date.today().year

        # excerpt (Выписка из ЕГРЮЛ/ЕГРИП)
        file_erg = requests.get(url_excerpt, allow_redirects=True)
        file_erg__filename = 'egr' + str(ogrn) + '.pdf'
        file_erg__relname  = os.path.join(upload_to, file_erg__filename)
        file_erg__fullname = os.path.join(settings.MEDIA_ROOT, upload_to, file_erg__filename)
        os.makedirs(os.path.join(settings.MEDIA_ROOT, upload_to), exist_ok=True)
        f1 = open( file_erg__fullname , 'wb', ).write(file_erg.content)


        inn = data[0]['inn']

        
        org.inn = inn
        org.ogrn = str(ogrn)

        org.short_name = data[0]['UL']['legalName']['short'] if 'short' in data[0]['UL']['legalName'] else data[0]['UL']['legalName']['full']
        org.full_name = data[0]['UL']['legalName']['full']

        org.basic = data
        org.egr_details = data_ergDetails
        org.analytics = data_analytics

        org.file_egr = file_erg__relname

        org.request_ver = request_ver
        org.save()

        # z = JSONasOrganiztion(data)
        # z = serializers.serialize("json", [z])
        # z = json.dumps(z,indent=2, default=str) 
        # z = data[0]

        # z['file_erg'] 

        # z['ergDetails'] = data_ergDetails[0]
        # z['analytics'] = data_analytics[0]
    except Exception as e:
        print(e)

    return org

def JSONasOrganiztion(json):

    d = json[0]

    org = Organization()
    org.inn = d['inn']

    return org
