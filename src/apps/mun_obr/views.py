import imp
from multiprocessing import context
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from apps.news.models import News

from apps.profile.models import Profile
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Statement,Mun_obr_news
from .serializers import *
from rest_framework import status

from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


def news(request):

    return render(request,'mun_obr/news/index.html')

class Get_news(APIView):
    def get(self,request):

        resp = Mun_obr_news.objects.values()

        return Response(resp)



def index(request):
    context = {"moderator":False}
    if "mun_obr_moder" in str(request.user.groups.all()):
        context = {"moderator":True}
    return render(request, 'mun_obr/vue/index.html',context=context)



# Получить данные профиля грантов       
class Get_profile(APIView):
    def get(self, request):
        user_id = request.user.id
        #prof = Profile.objects.filter(id=user_id).values()

        prof = Mun_obr_profile.objects.filter(author_id=user_id).values()
        if prof:
            return Response(prof)
        else:
            context = [{
                "mr_go_name":"",
                "sec_fio":"",
                "main_fio":"",
                "mail_jur":"",
                "phone_2":"",
                "ogrn":"",
                "inn":"",
                "jur_adrs":"",
                "bank_data":"",
                "author_id":request.user.id
            }]
            return Response(context)






class Mun_obr_profile_api(APIView):
    def post(self, request):
        s = request.data
        user_id = request.user.id
        c = Mun_obr_profile.objects.filter(author_id=user_id)
        serializer =Mun_obr_profileSerializer(data=s)
        if not c:
            
        
            if serializer.is_valid(raise_exception=True):
                resp = serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            
        else: 
            if serializer.is_valid(raise_exception=True):
                print(serializer.data)
                Mun_obr_profile.objects.filter(author_id=user_id).update(**serializer.data)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)



        
# Проекты пользователя по Id
class Get_projects(APIView):
  
    def get(self, request):
        user_id = request.user.id
        query = Statement.objects.filter(author_id=user_id).values()
        return Response(query)


# Проекты для модера
class Get_all_projects(APIView):
    def get(self,request):

        q = Statement.objects.filter(status="На модерации").values()
        return Response(q)

# Получть все проекты
class Get_all_statements(APIView):
  
    def get(self, request):
        # s = Statement.objects.all()
        # s = Statement_for_getSerializer(s, many=True)
        # return Response(s.data)
        q = Statement.objects.values()
        return Response(q)


class Get_contracts(APIView):
    def get(self, request,id):

        statement = Statement.objects.get(id=id)
        contract = statement.c_statementOf.values()
        return Response(contract[0])


class Create_statement(APIView):

    def post(self, request):
        article = request.data
        
        serializer = ArticleSerializer(data=article)
       
        if serializer.is_valid(raise_exception=True):
            resp = serializer.save()
        
        
        return Response({"success": "Article"})

    def put(self,request,*args,**kwargs):
        pk = kwargs.get("pk",None)
        if not pk:
            return Response({"error":"pk not allowed"})
        try:
            instance = Statement.objects.get(pk=pk)
        except:
            return Response({"error":"objects does not excists"})

        serializer = ArticleSerializer(data= request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"post":serializer.data})


class Create_contract(APIView):

    def post(self, request):
        article = request.data
        
        serializer = ContractSerializer(data=article)
       
        if serializer.is_valid(raise_exception=True):
            resp = serializer.save()
        
        
        return Response({"success": "Contract"})




class Send_messeges(APIView):

    def post(self, request):
        messege = request.data
        
        serializer = MessegeSerializer(data=messege)
       
        if serializer.is_valid(raise_exception=True):
            resp = serializer.save()
            messege_id = serializer.data['id']

            messege = Messeges.objects.filter(id=messege_id).values()
            return Response({"success": messege[0]})
        else:
            return Response({"error":"error_this"})

    def get(self, request,id):
        statement = Statement.objects.get(id=id)
        contract = statement.statement_chat.values().order_by('-id')
        return Response(contract)
