from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobPostingViewSet, ApplicationViewSet, InterviewViewSet, JobAppQuestionViewSet, JobAppAnswerViewSet

router = DefaultRouter()
router.register(r'job-postings', JobPostingViewSet, basename='job-postings')
router.register(r'applications', ApplicationViewSet, basename='applications')
router.register(r'interviews', InterviewViewSet, basename='interviews')
router.register(r'job-app-questions', JobAppQuestionViewSet, basename='job-app-questions')
router.register(r'job-app-answers', JobAppAnswerViewSet, basename='job-app-answers')


urlpatterns = [
    path('', include(router.urls)),
]