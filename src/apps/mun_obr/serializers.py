from dataclasses import field
from operator import mod
from pyexpat import model
from rest_framework import serializers
from .models import Statement, Contract, Messeges
from django.contrib.auth.models import User
from rest_framework import exceptions


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields =  ['title','requested_sum', 'sum_expenses', 'source','tab_1_file_1', 'link', 'recipient_type', 'ogrn', 'egryl_info', 'inn', 'kpp', 'full_name_grantee', 'short_name_grantee', 'd_f_name','d_s_name','d_m_name','d_position','d_phone','d_mail','d_amount_of_overdue_debt','author','file','status','comment']
    def to_representation(self, instance):
        self.fields['user'] =  UserSerializer(read_only=True)
        return super(ArticleSerializer, self).to_representation(instance)

    def update(self, instance, validatet_data):
        instance.status = validatet_data.get("status", instance.status)
        instance.requested_sum = validatet_data.get("requested_sum", instance.requested_sum)
        instance.sum_expenses = validatet_data.get("sum_expenses", instance.sum_expenses)
        instance.source = validatet_data.get("source", instance.source)
        instance.link = validatet_data.get("link", instance.link)
        instance.recipient_type = validatet_data.get("recipient_type", instance.recipient_type)
        instance.ogrn = validatet_data.get("ogrn", instance.ogrn)
        instance.egryl_info = validatet_data.get("egryl_info", instance.egryl_info)
        instance.inn = validatet_data.get("inn", instance.inn)
        instance.kpp = validatet_data.get("kpp", instance.kpp)
        instance.full_name_grantee = validatet_data.get("full_name_grantee", instance.full_name_grantee)
        instance.short_name_grantee = validatet_data.get("short_name_grantee", instance.short_name_grantee)
        instance.d_f_name = validatet_data.get("d_f_name", instance.d_f_name)
        instance.d_s_name = validatet_data.get("d_s_name", instance.d_s_name)
        instance.d_m_name = validatet_data.get("d_m_name", instance.d_m_name)
        instance.d_position = validatet_data.get("d_position", instance.d_position)
        instance.d_phone = validatet_data.get("d_phone", instance.d_phone)
        instance.d_mail = validatet_data.get("d_mail", instance.d_mail)
        instance.d_amount_of_overdue_debt = validatet_data.get("d_amount_of_overdue_debt", instance.d_amount_of_overdue_debt)
        instance.comment = validatet_data.get("comment", instance.comment)
        instance.save()
        return instance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    c_statement = serializers.PrimaryKeyRelatedField(queryset=Statement.objects.all())
    class Meta:
        model = Contract
        fields = ['c_checking_account', 'c_bik', 'c_bank_name','c_correspondent_account','c_recipient_type','c_ogrn','c_full_org_name','c_short_org_name','c_jur_adress','c_fact_adress','c_inn','c_kpp','c_tel','c_mail','c_f_name','c_s_name','c_m_name','c_position','c_operates_on_the_basis','c_pdf_file','c_pdf_file_name','c_statement']
  

class Statement_for_getSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields=['id','title']



class MessegeSerializer(serializers.ModelSerializer):
    statement_id = serializers.PrimaryKeyRelatedField(queryset=Statement.objects.all())
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Messeges
        fields = ['id','messege','statement_id','author','user_file']
  