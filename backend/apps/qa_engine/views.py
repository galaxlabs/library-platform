from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Query
from .serializers import AskQuestionSerializer, QuerySerializer
from .services import generate_grounded_answer


class QuestionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuerySerializer

    def get_queryset(self):
        return Query.objects.filter(user=self.request.user).prefetch_related(
            'answers__retrieved_sources__book',
            'answers__retrieved_sources__chunk',
        )

    def create(self, request, *args, **kwargs):
        serializer = AskQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = generate_grounded_answer(
            user=request.user,
            question=serializer.validated_data['question'],
            language_pair=serializer.validated_data['language_pair'],
            scope=serializer.validated_data.get('scope', 'general'),
            subject=serializer.validated_data.get('subject', ''),
            book_public_id=serializer.validated_data.get('book_public_id'),
            institute_public_id=serializer.validated_data.get('institute_public_id'),
        )
        return Response(QuerySerializer(query).data, status=status.HTTP_201_CREATED)


class QuestionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = QuerySerializer
    lookup_field = 'public_id'

    def get_queryset(self):
        return Query.objects.filter(user=self.request.user).prefetch_related(
            'answers__retrieved_sources__book',
            'answers__retrieved_sources__chunk',
        )


class ChatView(QuestionListCreateView):
    pass
