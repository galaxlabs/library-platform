from django.db.models import Count, Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from apps.analytics.services import track_event

from .models import Book, BookChunk, BookFile, BookReference
from .selectors import visible_books_queryset, visible_chunks_queryset
from .serializers import (
    BookChunkSerializer,
    BookCreateSerializer,
    BookDetailSerializer,
    BookFileSerializer,
    BookListSerializer,
    BookReferenceSerializer,
)


class BookListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BookCreateSerializer
        return BookListSerializer

    def get_queryset(self):
        queryset = visible_books_queryset(self.request.user).annotate(
            files_count=Count('files', distinct=True),
            chunks_count=Count('chunks', distinct=True),
        )
        params = self.request.query_params
        search = params.get('search')
        subject = params.get('subject')
        level = params.get('level')
        language = params.get('language')
        visibility = params.get('visibility')
        institute = params.get('institute')
        review_status = params.get('review_status')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(arabic_title__icontains=search)
                | Q(author__icontains=search)
                | Q(arabic_author_name__icontains=search)
                | Q(topic_tags__icontains=search)
            )
        if subject:
            queryset = queryset.filter(primary_subject__public_id=subject)
        if level:
            queryset = queryset.filter(level__iexact=level)
        if language:
            queryset = queryset.filter(language__iexact=language)
        if visibility:
            queryset = queryset.filter(visibility=visibility)
        if institute:
            queryset = queryset.filter(institute__public_id=institute)
        if review_status:
            queryset = queryset.filter(review_status=review_status)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        track_event(
            'book_created',
            user=request.user,
            payload={
                'book_public_id': str(book.public_id),
                'visibility': book.visibility,
                'review_status': book.review_status,
            },
        )
        output = BookDetailSerializer(book, context=self.get_serializer_context()).data
        return Response(output, status=status.HTTP_201_CREATED)


class BookDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookDetailSerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        return visible_books_queryset(self.request.user).prefetch_related(
            'files',
            'metadata_versions',
        )


class BookFileListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookFileSerializer

    def get_queryset(self):
        return BookFile.objects.filter(
            book__public_id=self.kwargs['public_id'],
            book_id__in=visible_books_queryset(self.request.user).values('id'),
        )


class BookChunkListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookChunkSerializer

    def get_queryset(self):
        queryset = visible_chunks_queryset(self.request.user).filter(book__public_id=self.kwargs['public_id'])
        chunk_type = self.request.query_params.get('chunk_type')
        if chunk_type:
            queryset = queryset.filter(chunk_type=chunk_type)
        return queryset.order_by('page_number', 'created_at')


class BookReferenceListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookReferenceSerializer

    def get_queryset(self):
        visible_ids = visible_books_queryset(self.request.user).values('id')
        return BookReference.objects.filter(
            Q(source_book__public_id=self.kwargs['public_id']) | Q(target_book__public_id=self.kwargs['public_id']),
            source_book_id__in=visible_ids,
            target_book_id__in=visible_ids,
        ).select_related('source_book', 'target_book')
