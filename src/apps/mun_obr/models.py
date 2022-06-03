from itertools import chain
from msilib.schema import Class
from operator import mod
from pyexpat import model
from statistics import mode
from turtle import title
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Statement(models.Model):
    status_choises = [
        ('На модерации','На модерации'),
        ('На доработке', 'На доработке'),
        ('Проверка пройдена', 'Проверка пройдена'),
    ]

    title = models.CharField("Название", max_length=255,blank=True)
    requested_sum = models.BigIntegerField("Запрашиваемая сумма гранта",blank=True, default=0)
    sum_expenses = models.BigIntegerField("Сумма расходов", blank=True,default=0)
    source = models.CharField("Источник (источники)", max_length=255,blank=True)
    #3 пункт
    tab_1_file_1 = models.FileField("Файл 1",upload_to='mun_obr_files' ,blank=True)
    link = models.CharField("Сайт в сети Интернет", max_length=255,blank=True)
    recipient_type = models.CharField("Тип получателя софинансирования", max_length=255,blank=True)
    ogrn = models.CharField("ОГРН", max_length=255,blank=True)
    egryl_info = models.CharField("Сведения из ЕГРЮЛ", max_length=255,blank=True)
    inn = models.CharField("ИНН", max_length=255,blank=True)
    kpp = models.CharField("КПП", max_length=255,blank=True)
    full_name_grantee = models.CharField("Полное наименование получателя гранта", max_length=255,blank=True)
    short_name_grantee = models.CharField("Сокращенное наименование получателя", max_length=255,blank=True)
    d_f_name = models.CharField("Имя руководителя", max_length=255,blank=True)
    d_s_name = models.CharField("Фамилия руководителя", max_length=255,blank=True)
    d_m_name = models.CharField("Отчество руководителя", max_length=255,blank=True)
    d_position = models.CharField("Должность руководителя", max_length=255,blank=True)
    d_phone = models.CharField("Телефон руководителя", max_length=255,blank=True)
    d_mail = models.CharField("Почта руководителя", max_length=255,blank=True)
    d_amount_of_overdue_debt = models.CharField("Сумма просроченной задолженности", max_length=255,blank=True)
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE, blank=True)
    status = models.CharField('Статус заявки',choices=status_choises,default="На модерации",max_length=100)
    comment = models.CharField('Комментарий',max_length=250,blank=True)

  

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
   

class Messeges(models.Model):
    create_time = models.DateTimeField('Дата добавления', auto_now_add=True)
    messege = models.CharField(max_length=255,blank=True)
    statement_id = models.ForeignKey(Statement,on_delete=models.CASCADE, blank=True,related_name='statement_chat')
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='user')
    user_file= models.FileField(upload_to='documents',blank=True)


class Mun_obr_profile(models.Model):
        #Муницыпальным образованиям 

    mr_go_name = models.CharField("Наименование МР/ГО", max_length=255, blank=True)
    main_fio = models.CharField("ФИО лица, имеющего право подписи без доверенности",max_length=255,blank=True)
    sec_fio = models.CharField("ФИО ответственного специалиста по взаимодействию с уполномоченным органом", max_length=255, blank=True)
    mail_jur = models.CharField("Адрес электронной почты для направления юридически значимых документов;", max_length=255, blank=True)
    phone_2 = models.CharField("Контактный телефон", max_length=255, blank=True)
    ogrn = models.CharField("ОГРН организации", max_length=255, blank=True)
    inn = models.CharField("ИНН организации", max_length=255, blank=True)
    jur_adrs = models.CharField("Юридический адрес", max_length=255, blank=True)
    bank_data = models.CharField("Банковские реквизиты ", max_length=255, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='user_1')


class Mun_obr_news(models.Model):

    title = models.CharField("Заголовок",max_length=255)
    img = models.ImageField(upload_to='mun_obr_news/%Y/%m/%d', verbose_name='Картинка', default=None, blank=True, null=True)
    content = models.TextField(verbose_name="Текст новости", default=None, blank=True, null=True)
    create_time = models.DateTimeField(auto_now=True)