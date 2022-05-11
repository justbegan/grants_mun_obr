from . import views
from django.urls import path

urlpatterns = [
    path('', views.NewsList.as_view(), name='news'),
    path('<int:pk>/', views.NewsDetail.as_view(), name='news_detail'),
]