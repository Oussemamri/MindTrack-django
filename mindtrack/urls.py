"""
URL configuration for mindtrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from quiz_app.views import home

urlpatterns = [
    path('', home, name='home'),  # Add this line for the home page
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('paths/', include('learning_paths.urls', namespace='learning_paths')),
    path('quizzes/', include('quiz_app.urls')),  # Changed from '' to 'quizzes/'
    path('study-sessions/', include('study_sessions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
