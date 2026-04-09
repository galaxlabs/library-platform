from django.urls import path

from .views import UploadSessionDetailView, UploadSessionListCreateView

urlpatterns = [
    path('jobs/', UploadSessionListCreateView.as_view(), name='ingestion-job-list'),
    path('jobs/<uuid:public_id>/', UploadSessionDetailView.as_view(), name='ingestion-job-detail'),
]
