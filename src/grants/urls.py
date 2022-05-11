"""grants URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.conf import settings 
from django.conf.urls.static import static
import notifications.urls

admin.site.site_header = "Панель администрирования"
admin.site.site_title = "Гранты"
admin.site.index_title = "Добро пожаловать"

urlpatterns = [
    path('', include('apps.contest.urls')),
    path('contest/', include('apps.contest.urls')),
    path('project/', include('apps.project.urls')),
    path('news/', include('apps.news.urls')),
    path('faq/', include('apps.faq.urls')),
    path('online-course/', include('apps.course.urls')),
    path('user/', include('apps.user.urls')),
    path('expert/', include('apps.expert.urls')),
    path('profile/', include('apps.profile.urls')),
    path('manage/', include('apps.manage.urls')),
    path('admin/', admin.site.urls),
    #path('accounts/', include('django.contrib.auth.urls')), 
    path('accounts/', include('allauth.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('page/', include('apps.page.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('contur/', include('apps.contur.urls')),
    path('mun_obr/', include('apps.mun_obr.urls')),
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
