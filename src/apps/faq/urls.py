from . import views
from django.urls import path

urlpatterns = [
    path('', views.FaqList.as_view(), name='faq'),
]