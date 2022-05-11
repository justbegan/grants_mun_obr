from . import views
from django.urls import path

urlpatterns = [
    path('', views.ContestHome.as_view(), name='contest-home'),
    path('directions/<slug:slug>/', views.DirectionDetails.as_view(), name='direction-details'),
    path('documents/', views.DocumentsView.as_view(), name='documents'),
    path('commission/', views.CommissionList.as_view(), name='commission'),
]