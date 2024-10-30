from django.urls import path
from . import views

app_name = 'study_sessions'

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path('create/', views.session_create, name='session_create'),
    path('<int:pk>/', views.session_detail, name='session_detail'),
    path('<int:pk>/edit/', views.session_update, name='session_update'),
    path('<int:pk>/delete/', views.session_delete, name='session_delete'),
    path('<int:pk>/activity/add/', views.add_activity, name='add_activity'),
    path('<int:pk>/complete/', views.complete_session, name='complete_session'),
    path('<int:pk>/pause/', views.pause_session, name='pause_session'),
    path('<int:pk>/resume/', views.resume_session, name='resume_session'),
] 