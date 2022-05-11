from . import views
from django.urls import path

urlpatterns = [
    path('', views.CourseList.as_view(), name='course'),
    path('<int:pk>/', views.CourseDetail.as_view(), name='course_detail'),
]