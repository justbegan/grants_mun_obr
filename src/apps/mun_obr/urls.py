from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter


router = SimpleRouter()



urlpatterns = [
    #Новости index
    path('',views.news,name='mun_obr_news'),
    #Новости api
    path('api/get_news',views.Get_news.as_view()),
    #ЛК index
    path('lc',views.index, name="lc"),
    #Профили api
    path('api/get_profile',views.Get_profile.as_view()),
    #Заявки пользователя
    path('api/get_projects',views.Get_projects.as_view()),
    #Получение контрактов  
    path('api/get_contracts/<int:id>',views.Get_contracts.as_view()),
    #Создать заявку
    path('api/create_statement',views.Create_statement.as_view()),
    #Создать контракт
    path('api/create_contract',views.Create_contract.as_view()),
    #Получить все заявки
    path('api/get_statements',views.Get_all_statements.as_view()),
    #Заявки модера
    path('api/get_all_projects',views.Get_all_projects.as_view()),
    #Обновление заявки
    path('api/statement_update/<int:pk>',views.Create_statement.as_view()),
    #Диалог
    path('api/create_messege',views.Send_messeges.as_view()),
    path('api/get_messeges/<int:id>',views.Send_messeges.as_view()),
    #Обновить или создать профиль mun_obr
    path('api/mun_obr_profile',views.Mun_obr_profile_api.as_view())
  

]

urlpatterns += router.urls