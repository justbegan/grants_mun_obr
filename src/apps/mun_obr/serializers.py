from dataclasses import field
from operator import mod
from pyexpat import model
from rest_framework import serializers
from .models import Statement, Contract
from django.contrib.auth.models import User



class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statement
        fields =  ['title','requested_sum', 'sum_expenses', 'source', 'link', 'recipient_type', 'ogrn', 'egryl_info', 'inn', 'kpp', 'full_name_grantee', 'short_name_grantee', 'director', 'director_position','author','file']
    def to_representation(self, instance):
        self.fields['user'] =  UserSerializer(read_only=True)
        return super(ArticleSerializer, self).to_representation(instance)

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

