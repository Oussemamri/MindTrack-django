from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import CustomLoginView, register

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        next_page='accounts:login',
        template_name=None
    ), name='logout'),
    path('register/', register, name='register'),
] 