from django.db.models import Q
from django.views import generic

from .models import Faq


class FaqList(generic.ListView):
    queryset = Faq.objects.order_by('-created_on')
    template_name = 'faq/index.html'
    paginate_by = 10

    def get_queryset(self):

        from django.contrib.auth.models import User
        # u = User.objects.get(id=1162)
        # notify.send(request.user, recipient=project.author, verb='Заявка отправлена на доработку', action=project)
        # project = Project.objects.get(id=1245)
        # print(z)
        # u.set_password('12345')
        # u.save()
        # u = User.objects.get(id=58)
        # u.set_password('12345')
        # u.save()
        # print(u)

        query = self.request.GET.get('q')
        if query:
            self.queryset = self.queryset.filter(
                Q(question__icontains=query) | Q(answer__icontains=query)
            )
        return self.queryset

