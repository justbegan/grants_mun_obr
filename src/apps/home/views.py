from django.shortcuts import render
from django.views import generic

class HomePage(generic.View):
    '''Главная страница'''
    def get(self, request):
        return render(request, "index.html")