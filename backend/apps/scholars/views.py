from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.analytics.services import track_event
from apps.qa_engine.models import Answer

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
        review = serializer.save()
        track_event(
            'scholar_review_submitted',
            user=self.request.user,
            payload={
                'review_id': review.id,
                'answer_public_id': str(review.answer.public_id),
                'decision': review.decision,
            },
        )


class ScholarReviewQueueView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        scholar = getattr(request.user, 'scholar_profile', None)
        if not request.user.is_staff and not request.user.is_superuser:
            if not scholar or scholar.verification_status != 'verified':
                raise permissions.PermissionDenied('Only verified scholars can view the scholar review queue.')

        queryset = (
            ScholarReview.objects.select_related('answer', 'answer__query', 'scholar')
            .order_by('-created_at')
        )
        recent_reviews = ScholarReviewSerializer(queryset[:10], many=True).data

        pending_answers = Answer.objects.filter(verification_status='needs_review').select_related('query')[:10]
        pending_payload = [
            {
                'answer_public_id': str(answer.public_id),
                'question': answer.query.question,
                'verification_status': answer.verification_status,
                'confidence': str(answer.confidence),
                'created_at': answer.created_at,
            }
            for answer in pending_answers
        ]
        return Response({'pending_answers': pending_payload, 'recent_reviews': recent_reviews})
