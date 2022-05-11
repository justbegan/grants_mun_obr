from django.shortcuts import render
from django.views import generic
from .models import News


class NewsList(generic.ListView):
    queryset = News.objects.order_by('-created_on')
    template_name = 'news/index.html'


class NewsDetail(generic.DetailView):
    model = News
    template_name = 'news/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_list = list(News.get_list(4))
        if self.object in news_list:
            news_list.remove(self.object)
        else:
            news_list.pop()
        context['news_list'] = news_list
        return context

