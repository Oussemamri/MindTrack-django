from django.urls import path
from . import views

app_name = 'learning_paths'

urlpatterns = [
    path('', views.path_list, name='path_list'),
    path('create/', views.create_path, name='create_path'),
    path('<int:path_id>/', views.path_detail, name='path_detail'),
    path('<int:path_id>/edit/', views.edit_path, name='edit_path'),
    path('<int:path_id>/delete/', views.delete_path, name='delete_path'),
    path('<int:path_id>/enroll/', views.enroll_path, name='enroll_path'),
    path('<int:path_id>/continue/', views.continue_path, name='continue_path'),
    path('api/topics/<int:topic_id>/quizzes/', views.get_topic_quizzes, name='topic_quizzes'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('ai-assistant/', views.ai_assistant, name='ai_assistant'),

]