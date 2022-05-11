from django.db.models import Q
from django.views import generic

from .models import Course


class CourseList(generic.ListView):
    queryset = Course.objects.order_by('-created_on')
    template_name = 'course/index.html'
    # paginate_by = 10

    # def get_queryset(self):
    #     query = self.request.GET.get('q')
    #     if query:
    #         self.queryset = self.queryset.filter(
    #             Q(question__icontains=query) | Q(answer__icontains=query)
    #         )
    #     return self.queryset


class CourseDetail(generic.DetailView):
    model = Course
    template_name = 'course/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     news_list = list(News.get_list(4))
    #     if self.object in news_list:
    #         news_list.remove(self.object)
    #     else:
    #         news_list.pop()
    #     context['news_list'] = news_list
    #     return context

