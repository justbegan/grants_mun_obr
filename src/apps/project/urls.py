from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='project-home'),
    path('vote-projects', views.vote_projects, name='project-vote-projects'),
    path('best-projects', views.best_projects, name='project-best-projects'),
    path("view/<int:id>/", views.view, name="project-view"),
    path("vote/<int:project_id>/", views.vote, name="project-vote"),
    path("user-vote/<int:project_id>/", views.user_vote, name="project-user-vote"),
    path("pdf/<int:project_id>/", views.project_pdf, name="project-pdf"),
    path("cron", views.cron),
    path("test", views.test)
]