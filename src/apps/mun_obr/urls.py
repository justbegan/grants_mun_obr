from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register('api/order',views.Get_list)


urlpatterns = [
    path('', views.NewsList.as_view(), name='news_obr'),
    path('test/',views.index, name="mun_obr_profile"),
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
  

]

urlpatterns += router.urls