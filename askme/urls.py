"""askme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from question import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('question.urls', namespace='question')),
    # path('', views.IndexView.as_view(), name='index-view'),
    # path('hot/', views.HotView.as_view(), name='hot-view'),
    # path('question/<int:pk>/', views.QuestionView.as_view(),
    #      name='question-view'),
    # path('question/new/', views.QuestionCreateView.as_view(),
    #      name='new-question-view'),
    # path('tag/<int:pk>/', views.TagView.as_view(), name='tag-view'),
    # path('profile/<int:pk>/', views.ProfileView.as_view(),
    #      name='profile-view'),
    # path('profile/<int:pk>/edit/', views.ProfileEditView.as_view(),
    #      name='profile-edit-view'),
    # path('login/', views.LoginAjaxView.as_view(), name='login-view'),
    # path('signup/', views.SignupView.as_view(), name='signup-view'),
    # path('admin/', admin.site.urls),
    # path(f'{settings.MEDIA_URL}<str:path>', serve, {
    #     'document_root': settings.MEDIA_ROOT})
]
