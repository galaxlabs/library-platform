from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.analytics.services import track_event

from .models import UploadSession
from .serializers import CreateIngestionJobSerializer, UploadSessionSerializer
from .services import enqueue_ingestion_job
from .tasks import run_upload_pipeline


class UploadSessionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UploadSession.objects.select_related('book', 'initiated_by').prefetch_related(
            'stage_runs',
            'tasks',
        )
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(initiated_by=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateIngestionJobSerializer
        return UploadSessionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()
        enqueue_ingestion_job(session)
        run_upload_pipeline.delay(session.id)
        track_event(
            'ingestion_job_created',
            user=request.user,
            payload={'upload_session_public_id': str(session.public_id), 'book_public_id': str(session.book.public_id)},
        )
        output = UploadSessionSerializer(session, context=self.get_serializer_context()).data
        return Response(output, status=status.HTTP_201_CREATED)


class UploadSessionDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UploadSessionSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        queryset = UploadSession.objects.select_related('book', 'initiated_by').prefetch_related(
            'stage_runs',
            'tasks',
        )
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        return queryset.filter(initiated_by=self.request.user)
