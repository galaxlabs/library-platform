from rest_framework import generics, permissions

from apps.common.permissions import IsScholar

from .models import Scholar, ScholarReview
from .serializers import ScholarApplicationSerializer, ScholarReviewSerializer, ScholarSerializer


class ScholarProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScholarSerializer

    def get_object(self):
        scholar, _ = Scholar.objects.get_or_create(
            user=self.request.user,
            defaults={
                'full_name': self.request.user.full_name,
                'arabic_name': self.request.user.arabic_name,
            },
        )
        return scholar


class ScholarApplicationView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ScholarApplicationSerializer
        return ScholarSerializer

    def get_queryset(self):
        queryset = Scholar.objects.all().select_related('user')
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset.filter(verification_status__in=['pending', 'under_review', 'rejected', 'verified'])
        return queryset.filter(user=self.request.user)


class ScholarReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ScholarReviewSerializer

    def get_queryset(self):
        queryset = ScholarReview.objects.select_related('scholar', 'answer', 'answer__query')
        if self.request.user.is_staff or self.request.user.is_superuser:
            return queryset
        scholar = getattr(self.request.user, 'scholar_profile', None)
        if scholar:
            return queryset.filter(scholar=scholar)
        return queryset.none()

    def perform_create(self, serializer):
        scholar = getattr(self.request.user, 'scholar_profile', None)
        if not scholar or scholar.verification_status != 'verified':
            raise permissions.PermissionDenied('Only verified scholars can submit reviews.')
        serializer.save()
