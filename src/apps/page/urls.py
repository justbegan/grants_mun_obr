from . import views
from django.urls import path

urlpatterns = [
    path('<slug:slug>/', views.PageView.as_view(), name='page'),
]