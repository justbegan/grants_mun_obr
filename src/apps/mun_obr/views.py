import imp
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render
from django.views import generic
from apps.news.models import News

from apps.profile.models import Profile
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Statement
from .serializers import *
from rest_framework import status

# Create your views here.
class NewsList(generic.ListView):
    queryset = News.objects.order_by('-created_on').filter(for_munobr=True)
    template_name = 'news/index.html'



from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet





def notifies(request):
    notifications = request.user.notifications
    context = {
        'read': notifications.read(),
        'unread': notifications.unread()
    }
    for notify in notifications.unread():
        notify.mark_as_read()

    return render(request, 'mun_obr/profile/notifies.html',context)



def vue_test(request):


    return render(request, 'mun_obr/vue/index.html')



# Получить данные профиля грантов       
class Get_profile(APIView):
    def get(self, request):
        user_id = request.user.id
        #prof = Profile.objects.filter(id=user_id).values()
        prof = Mun_obr_profile.objects.filter(author_id=user_id).values()
        return Response(prof)






class Mun_obr_profile_api(APIView):
    def post(self, request):
        s = request.data
        user_id = request.user.id
        c = Mun_obr_profile.objects.filter(author_id=user_id)
        serializer =Mun_obr_profileSerializer(data=s)
        print()
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



        

class Get_projects(APIView):
  
    def get(self, request):
        user_id = request.user.id
        q = Statement.objects.filter(author_id=user_id).values()
        return Response(q)
        # return Response(self.get_verbose_name(user_id))

    def get_verbose_name(self,user_id):
        #Get verbose_name from model
        f_name = Statement._meta.fields
        verbose_names = [i.verbose_name for i in f_name]

        v_list = [i for i in Statement.objects.filter(author_id=user_id).values_list()]

        return [ dict(zip(verbose_names, i)) for i in v_list ]

class Get_all_projects(APIView):
    def get(self,request):

        q = Statement.objects.filter(status="На модерации").values()
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


class Get_all_statements(APIView):
  
    def get(self, request):
        s = Statement.objects.all()
        s = Statement_for_getSerializer(s, many=True)
        return Response(s.data)



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
