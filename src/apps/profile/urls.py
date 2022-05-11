from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='profile-home'),
    path('notifies/', views.notifies, name='profile-notifies'),
]