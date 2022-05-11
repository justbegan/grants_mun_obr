from msilib.schema import Class
from operator import mod
from pyexpat import model
from turtle import title
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Statement(models.Model):

    title = models.CharField("Название", max_length=255,blank=True)
    requested_sum = models.IntegerField("Запрашиваемая сумма гранта", max_length=255,blank=True, default=0)
    sum_expenses = models.IntegerField("Сумма расходов", max_length=255,blank=True,default=0)
    source = models.CharField("Источник (источники)", max_length=255,blank=True)
    #3 пункт
    link = models.CharField("Сайт в сети Интернет", max_length=255,blank=True)
    recipient_type = models.CharField("Тип получателя софинансирования", max_length=255,blank=True)
    ogrn = models.CharField("ОГРН", max_length=255,blank=True)
    egryl_info = models.CharField("Сведения из ЕГРЮЛ", max_length=255,blank=True)
    inn = models.CharField("ИНН", max_length=255,blank=True)
    kpp = models.CharField("КПП", max_length=255,blank=True)
    full_name_grantee = models.CharField("Полное наименование получателя гранта", max_length=255,blank=True)
    short_name_grantee = models.CharField("Сокращенное наименование получателя", max_length=255,blank=True)
    director = models.CharField("ФИО руководителя", max_length=255,blank=True)
    director_position = models.CharField("ФИО руководителя", max_length=255,blank=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE, blank=True)
    file = models.FileField(upload_to='documents',max_length=100,blank=True)

  

class Contract(models.Model):
    c_checking_account= models.CharField(max_length=255,blank=True)
    c_bik= models.CharField(max_length=255,blank=True)
    c_bank_name= models.CharField(max_length=255,blank=True)
    c_correspondent_account= models.CharField(max_length=255,blank=True)
    c_recipient_type= models.CharField(max_length=255,blank=True)
    c_ogrn= models.CharField(max_length=255,blank=True)
    c_full_org_name= models.CharField(max_length=255,blank=True)
    c_short_org_name= models.CharField(max_length=255,blank=True)
    c_jur_adress= models.CharField(max_length=255,blank=True)
    c_fact_adress= models.CharField(max_length=255,blank=True)
    c_inn= models.CharField(max_length=255,blank=True)
    c_kpp= models.CharField(max_length=255,blank=True)
    c_tel= models.CharField(max_length=255,blank=True)
    c_mail= models.CharField(max_length=255,blank=True)
    c_f_name= models.CharField(max_length=255,blank=True)
    c_s_name= models.CharField(max_length=255,blank=True)
    c_m_name= models.CharField(max_length=255,blank=True)
    c_position= models.CharField(max_length=255,blank=True)
    c_operates_on_the_basis= models.CharField(max_length=255,blank=True)
    c_pdf_file= models.FileField(upload_to='documents',blank=True)
    c_pdf_file_name= models.CharField(max_length=255,blank=True)
    c_statement = models.ForeignKey(Statement,on_delete=models.CASCADE, blank=True,related_name='c_statementOf')
   

