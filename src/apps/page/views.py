from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Page
from ..contest.models import DocumentTag, Document
from ..project.services import get_open_contest


class PageView(generic.View):

    def get(self, request, slug):
        page = get_object_or_404(Page, slug=slug)
        documents = None
        related_pages = None
        contest = get_open_contest()

        if page.related_tag:
            documents = Document.objects.filter(tags=page.related_tag, contest=contest).prefetch_related('tags').all()
            # tags = DocumentTag.objects.filter(is_main=True).all()
            related_pages = Page.objects.filter(related_tag__isnull=False).all()
        context = {
            'page': page,
            'documents': documents,
            'related_pages': related_pages
        }
        return render(request, "page/view.html", context)

