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

from .forms import UserForm, ProfileForm
# Create your views here.
class NewsList(generic.ListView):
    queryset = News.objects.order_by('-created_on').filter(for_munobr=True)
    template_name = 'news/index.html'



from rest_framework.serializers import ModelSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet




def index(request):
    # if request.method == 'POST':
    #     user_form = UserForm(request.POST, instance=request.user)
    #     profile_form = ProfileForm(request.POST, instance=request.user.profile)
    #     if user_form.is_valid() and profile_form.is_valid():
    #         user_form.save()
    #         profile_form.save()
    #         messages.success(request, 'Ваш профиль был успешно обновлен!')
    #         return redirect('profile-home')
    #     else:
    #         messages.error(request, 'Пожалуйста, исправьте ошибки.')
    # else:
    #     user_form = UserForm(instance=request.user)
    #     profile_form = ProfileForm(instance=request.user.profile)
    # return render(request, 'profile/index.html', {
    #     'user_form': user_form,
    #     'profile_form': profile_form
    # })

    from allauth.account.views import PasswordChangeView
    from allauth.account.forms import ChangePasswordForm
    from allauth.account.utils import logout_on_password_change

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if request.POST.get('pwd'):
            pwd_form = ChangePasswordForm(data=request.POST, user=request.user)
            if pwd_form.is_valid():
                v = PasswordChangeView.as_view(success_url=reverse_lazy('profile-home'))
                # v.success_url = 'profile-home'
                return v(request)
                # logout_on_password_change(request, pwd_form.user)
                # return redirect('profile-home')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки.')
        else:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Ваш профиль был успешно обновлен!')
                return redirect('profile-home')
            else:
                messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        pwd_form = ChangePasswordForm(user=request.user)
    return render(request, 'mun_obr/profile/index.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'pwd_form': pwd_form
    })


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




class Main_app_serializers(ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','mr_go_name','main_fio','sec_fio','mail_jur','phone_2','ogrn','inn','jur_adrs','bank_data']

class Statement_serializers(ModelSerializer):
    class Meta:
        model = Statement
        fields = ['id','title','requested_sum', 'sum_expenses', 'source', 'link', 'recipient_type', 'ogrn', 'egryl_info', 'inn', 'kpp', 'full_name_grantee', 'short_name_grantee', 'director', 'director_position']



class Get_list(ModelViewSet):
  
    queryset = Profile.objects.filter(id='541').all()
    serializer_class = Main_app_serializers
 
        
class Get_profile(APIView):
    def get(self, request):
        user_id = request.user.id
        prof = Profile.objects.filter(id=user_id)
        serializer = Main_app_serializers(prof, many=True)
        return Response(serializer.data)

    
        

class Get_projects(APIView):
  
    def get(self, request):
        user_id = request.user.id

        return Response(self.get_verbose_name(user_id))

    def get_verbose_name(self,user_id):
        #Get verbose_name from model
        f_name = Statement._meta.fields
        verbose_names = [i.verbose_name for i in f_name]

        v_list = [i for i in Statement.objects.filter(author_id=user_id).values_list()]

        return [ dict(zip(verbose_names, i)) for i in v_list ]


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
