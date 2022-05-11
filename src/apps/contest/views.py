from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Direction, Contest, Document, DocumentTag, Commission
from django.core.exceptions import ObjectDoesNotExist
from apps.project.services import get_open_contest

from ..news.models import News


class ContestHome(generic.View):
    
    def get(self, request):
        contest = get_open_contest()
        directions = contest.directions.all()
        news_list = News.get_list(4)

        context = {
            'directions': directions,
            'contest': contest,
            'news_list': news_list,
            'docs': Document.objects.filter(tags__slug='contest', contest=contest).all()
        }
        
        return render(request, "contest/index.html", context)


class DirectionDetails(generic.View):
    def get(self, request, slug):
        direction = get_object_or_404(Direction, slug=slug)
        context = {
            'direction': direction,
        }
        return render(request, "contest/direction_details.html", context)


class DocumentsView(generic.View):
    def get(self, request):
        current_tag = request.GET.get('tag')
        contest = get_open_contest()
        if current_tag:
            current_tag = get_object_or_404(DocumentTag, slug=current_tag)
            documents = Document.objects.filter(tags=current_tag, contest=contest).prefetch_related('tags').all()
        else:
            documents = Document.objects.exclude(tags__is_hidden=True).filter(contest=contest).prefetch_related('tags').all()
        tags = DocumentTag.objects.exclude(is_hidden=True).all()
        context = {
            'documents': documents,
            'tags': tags,
            'current_tag': current_tag
        }
        return render(request, "contest/documents.html", context)


class CommissionList(generic.View):

    def get(self, request):
        boss = Commission.objects.filter(boss=True).all()[0]
        commission_list = Commission.objects.all().exclude(boss=True).order_by('order_field')
        context = {
            'boss': boss,
            'commission_list': commission_list,
        }

        return render(request, "contest/commission-list.html", context)

