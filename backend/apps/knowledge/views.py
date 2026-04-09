from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.library.models import BookTopicMap

from .models import KnowledgeObject
from .serializers import KnowledgeObjectSerializer


class KnowledgeObjectListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = KnowledgeObjectSerializer

    def get_queryset(self):
        queryset = KnowledgeObject.objects.filter(is_published=True).select_related(
            'book',
            'chunk',
            'skill_pack',
            'subject',
        )
        params = self.request.query_params
        if params.get('book'):
            queryset = queryset.filter(book__public_id=params['book'])
        if params.get('type'):
            queryset = queryset.filter(object_type=params['type'])
        if params.get('topic'):
            queryset = queryset.filter(topic__icontains=params['topic'])
        return queryset


class KnowledgeObjectDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = KnowledgeObjectSerializer
    lookup_field = 'public_id'
    queryset = KnowledgeObject.objects.filter(is_published=True).select_related(
        'book',
        'chunk',
        'skill_pack',
        'subject',
    )


class TopicMapListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = BookTopicMap.objects.all().select_related('book')
        book_id = request.query_params.get('book')
        if book_id:
            queryset = queryset.filter(book__public_id=book_id)
        data = [
            {
                'book_public_id': str(item.book.public_id),
                'book_title': item.book.title,
                'topics': item.topics,
                'concept_links': item.concept_links,
            }
            for item in queryset[:50]
        ]
        return Response(data)
