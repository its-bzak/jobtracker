from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from .models import JobPosting, Application, Interview
from .serializers import (JobPostingSerializer, ApplicationSerializer, InterviewSerializer)

# Create your views here.

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user)


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Application.objects.filter(
            Q(applicant=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

    def perform_update(self, serializer):
        application = self.get_object()
        if application.applicant != self.request.user:
            raise PermissionDenied("You do not have permission to edit this application.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.applicant != self.request.user:
            raise PermissionDenied("You do not have permission to delete this application.")
        instance.delete()



class InterviewViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Interview.objects.filter(
            Q(application__applicant=user)
        ).distinct()
