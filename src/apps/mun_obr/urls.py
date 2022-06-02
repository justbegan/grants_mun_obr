from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()



urlpatterns = [
    path('news',views.news,name='news'),
    path('api/get_news',views.Get_news.as_view()),
    path('vue_test/',views.vue_test, name="vue_test"),
    path('api/get_profile',views.Get_profile.as_view()),
    path('api/get_projects',views.Get_projects.as_view()),
    path('api/get_contracts/<int:id>',views.Get_contracts.as_view()),
    path('api/create_statement',views.Create_statement.as_view()),
    path('api/create_contract',views.Create_contract.as_view()),
    path('api/get_statements',views.Get_all_statements.as_view()),
    path('api/get_all_projects',views.Get_all_projects.as_view()),
    path('api/statement_update/<int:pk>',views.Create_statement.as_view()),
    path('api/create_messege',views.Send_messeges.as_view()),
    path('api/get_messeges/<int:id>',views.Send_messeges.as_view()),
    path('api/mun_obr_profile',views.Mun_obr_profile_api.as_view())
  

]

urlpatterns += router.urls