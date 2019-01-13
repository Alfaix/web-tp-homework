from django.urls import path
from django.conf import settings
from django.views.static import serve

from . import views

app_name = 'question'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index-view'),
    path('hot/', views.HotView.as_view(), name='hot-view'),
    path('question/<int:pk>/', views.QuestionView.as_view(),
         name='question-view'),
    path('question/new/', views.QuestionCreateView.as_view(),
         name='new-question-view'),
    path('tag/<int:pk>/', views.TagView.as_view(), name='tag-view'),
    path('profile/<int:pk>/', views.ProfileView.as_view(),
         name='profile-view'),
    path('profile/<int:pk>/edit/', views.ProfileEditView.as_view(),
         name='profile-edit-view'),

    path('signup/', views.SignupView.as_view(), name='signup'),

    path('ajax/login/', views.LoginAjaxView.as_view(), name='login-view'),
    path('ajax/logout/', views.LogoutAjaxView.as_view(), name='logout'),
    path('ajax/signup/', views.SignupAjaxView.as_view(), name='ajax_signup'),
    path('ajax/questions/<int:pk>/upvote/', views.QuestionUpvoteAjaxView.as_view(), name='ajax_question_upvote'),
    path('ajax/questions/<int:pk>/downvote/', views.QuestionDownvoteAjaxView.as_view(), name='ajax_question_downvote'),
    path('ajax/answers/<int:pk>/upvote/', views.AnswerUpvoteAjaxView.as_view(), name='ajax_answer_upvote'),
    path('ajax/answers/<int:pk>/downvote/', views.AnswerDownvoteAjaxView.as_view(), name='ajax_answer_downvote'),

    path(f'{settings.MEDIA_URL}<str:path>', serve, {
        'document_root': settings.MEDIA_ROOT})
]
