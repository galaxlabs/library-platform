from rest_framework import serializers

from .models import Answer, Query, RetrievedSource


class RetrievedSourceSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    book_public_id = serializers.UUIDField(source='book.public_id', read_only=True)
    book_title = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()
    chunk_public_id = serializers.UUIDField(source='chunk.public_id', read_only=True)

    class Meta:
        model = RetrievedSource
        fields = [
            'id',
            'public_id',
            'book_public_id',
            'book_title',
            'chunk_public_id',
            'page_number',
            'score',
            'retrieval_reason',
            'excerpt',
        ]

    def get_book_title(self, obj):
        if obj.book:
            return obj.book.arabic_title or obj.book.title
        return ''

    def get_excerpt(self, obj):
        if obj.chunk:
            return obj.chunk.content[:320]
        return ''


class AnswerSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    references = RetrievedSourceSerializer(source='retrieved_sources', many=True, read_only=True)
    explanation = serializers.CharField(source='detailed_explanation', read_only=True)
    simplified_explanation = serializers.CharField(read_only=True)
    examples = serializers.JSONField(source='generated_examples', read_only=True)

    class Meta:
        model = Answer
        fields = [
            'id',
            'public_id',
            'direct_answer',
            'explanation',
            'simplified_explanation',
            'examples',
            'verification_status',
            'confidence',
            'references',
            'created_at',
        ]


class QuerySerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    latest_answer = serializers.SerializerMethodField()

    class Meta:
        model = Query
        fields = [
            'id',
            'public_id',
            'question',
            'language_pair',
            'detected_subject',
            'detected_sub_subject',
            'detected_intent',
            'detected_level',
            'sensitivity_level',
            'search_scope',
            'verification_preference',
            'created_at',
            'latest_answer',
        ]

    def get_latest_answer(self, obj):
        answer = obj.answers.order_by('-created_at').first()
        if not answer:
            return None
        return AnswerSerializer(answer).data


class AskQuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=2000)
    language_pair = serializers.CharField(required=False, default='ar-en')
    scope = serializers.ChoiceField(
        choices=[('general', 'general'), ('subject', 'subject'), ('book', 'book'), ('institute', 'institute')],
        default='general',
        required=False,
    )
    subject = serializers.CharField(required=False, allow_blank=True)
    book_public_id = serializers.UUIDField(required=False)
    institute_public_id = serializers.UUIDField(required=False)
