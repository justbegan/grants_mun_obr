from . import views
from django.urls import path

urlpatterns = [
    path('', views.project_list, name='manage-home'),
    path('score-sheet-list/', views.score_sheet_list, name='manage-score-sheet-list'),
    path('edit-score-sheet/<int:id>', views.edit_score_sheet, name='manage-edit-score-sheet'),
    path('delete-score-sheet/<int:id>', views.delete_score_sheet, name='manage-delete-score-sheet'),
    path('assign-experts/<int:id>', views.assign_experts, name='manage-assign-experts'),
    path('project-to-fix/<int:id>', views.project_to_fix, name='manage-project-to-fix'),
    path('project-to-check/<int:id>', views.project_to_check, name='manage-project-to-check'),
    path('project-reject/<int:id>', views.project_reject, name='manage-project-reject'),
    path('project-win/<int:id>', views.project_win, name='manage-project-win'),
    path('project-not-win/<int:id>', views.project_not_win, name='manage-project-not-win'),

    path('report-list/', views.report_list, name='manage-report-list'),
    path('report-view/<int:project_id>', views.report_view, name='manage-report-view'),
    path('report-change-status/<int:project_id>/<str:status>', views.report_change_status, name='manage-report-change-status'),

    path('reporting-list/', views.reporting_list, name='manage-reporting-list'),
]
