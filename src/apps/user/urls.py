from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='user-home'),

    path('create-project/<int:contest_id>', views.create_project, name='user-create-project'),
    path('view-project/<int:id>', views.view_project, name='user-view-project'),
    path('view-expertise/<int:project_id>', views.view_expertise, name='user-view-expertise'),
    path('view-project/<int:id>#finish', views.view_project, name='user-view-project-finish'),
    path('edit-project/<int:id>', views.edit_project, name='user-edit-project'),
    path('save-project/<int:id>', views.save_project, name='user-save-project'),
    path('publish-project/<int:id>', views.publish_project, name='user-publish-project'),
    path('delete-project/<int:id>', views.delete_project, name='user-delete-project'),

    path('report-project/<int:project_id>', views.report_project, name='user-report-project'),
    path('report-list/', views.report_list, name='user-report-list'),
    path('report-save/<int:project_id>', views.save_report, name='user-save-report'),
    path('report-publish/<int:project_id>', views.publish_report, name='user-report-publish'),

    path('regions', views.regions, name='user-regions'),
    path('regions/<str:query>', views.regions, name='user-regions'),

    path('upload-file/<str:type>/<int:project_id>', views.upload_file, name='user-upload-file'),
    path('delete-file/<int:id>', views.delete_file, name='user-delete-file'),

    path('request-pdf/<int:project_id>', views.request_pdf, name='user-request-pdf'),
    path('fill-fields/<int:project_id>', views.fill_fields, name='user-fill-fields'),
    path('direction-max-sum/<int:project_id>', views.direction_max_sum, name='user-direction-max-sum'),
    path('agreements-project/<int:id>', views.agreements_project, name='user-agreements-project'),
    path('reporting-project/<int:id>', views.reporting_project, name='user-reporting-project'),
]
