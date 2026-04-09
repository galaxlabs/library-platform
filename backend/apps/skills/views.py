from rest_framework import generics, permissions

from .models import SkillPack
from .serializers import SkillPackSerializer


class SkillPackListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillPackSerializer

    def get_queryset(self):
        queryset = SkillPack.objects.prefetch_related('source_books')
        params = self.request.query_params
        if params.get('subject'):
            queryset = queryset.filter(subject__icontains=params['subject'])
        if params.get('review_status'):
            queryset = queryset.filter(review_status=params['review_status'])
        if params.get('active'):
            queryset = queryset.filter(active=params['active'].lower() == 'true')
        if params.get('book'):
            queryset = queryset.filter(source_books__public_id=params['book'])
        return queryset.distinct()


class SkillPackDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillPackSerializer
    lookup_field = 'public_id'
    queryset = SkillPack.objects.prefetch_related('source_books')
