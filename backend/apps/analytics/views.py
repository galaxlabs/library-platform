from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.ingestion.models import UploadSession
from apps.library.models import Book
from apps.qa_engine.models import Query
from apps.scholars.models import Scholar


class DashboardCountersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent_books = list(
            Book.objects.filter(uploaded_by=request.user).order_by('-created_at')[:5].values(
                'title',
                'public_id',
                'review_status',
                'visibility',
            )
        )
        recent_jobs = list(
            UploadSession.objects.filter(initiated_by=request.user).order_by('-created_at')[:5].values(
                'public_id',
                'status',
                'current_stage',
                'book__title',
            )
        )
        recent_queries = list(
            Query.objects.filter(user=request.user).order_by('-created_at')[:5].values(
                'public_id',
                'question',
                'detected_subject',
                'search_scope',
            )
        )
        counters = {
            'my_books': Book.objects.filter(uploaded_by=request.user).count(),
            'recent_books': recent_books,
            'ingestion_jobs': UploadSession.objects.filter(initiated_by=request.user).count(),
            'recent_ingestion_jobs': recent_jobs,
            'recent_queries_count': Query.objects.filter(user=request.user).count(),
            'recent_queries': recent_queries,
            'institutes_count': request.user.institute_memberships.filter(is_active=True).count(),
            'scholar_profile': None,
        }
        scholar = getattr(request.user, 'scholar_profile', None)
        if scholar:
            counters['scholar_profile'] = {
                'verification_status': scholar.verification_status,
                'review_count': scholar.review_count,
                'trust_score': str(scholar.trust_score),
            }
        if request.user.is_staff or request.user.is_superuser:
            counters['platform'] = {
                'books_total': Book.objects.count(),
                'books_under_review': Book.objects.filter(review_status='under_review').count(),
                'verified_scholars': Scholar.objects.filter(verification_status='verified').count(),
            }
        return Response(counters)
