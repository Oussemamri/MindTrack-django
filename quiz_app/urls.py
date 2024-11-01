from django.urls import path
from . import views

app_name = 'quiz_app'

urlpatterns = [
    path('', views.quiz_list, name='quiz_list'),
    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('submission/<int:submission_id>/results/', views.quiz_results, name='quiz_results'),
] 