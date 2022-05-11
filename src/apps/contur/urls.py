from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='contur-home'),
    path('api/req', views.api_req, name='contur-api-req'),
]