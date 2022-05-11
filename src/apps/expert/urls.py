from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='expert-home'),
    path('edit-score-sheet/<int:project_id>', views.edit_score_sheet, name='expert-edit-score-sheet'),
    path('delete-score-sheet/<int:id>', views.delete_score_sheet, name='expert-delete-score-sheet'),
    path('score-sheet-list/', views.score_sheet_list, name='expert-score-sheet-list'),
    path('view-score-sheet/<int:id>', views.view_score_sheet, name='expert-view-score-sheet'),
    path('finish-score-sheet/<int:id>', views.finish_score_sheet, name='expert-finish-score-sheet'),
    path('documents/', views.documents, name='expert-documents'),
]