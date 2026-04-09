from rest_framework import serializers

from apps.library.models import Book

from .models import IngestionStageRun, UploadSession, UploadTask
from .services import create_ingestion_job


class IngestionStageRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngestionStageRun
        fields = ['stage', 'status', 'diagnostics', 'operator_notes', 'created_at', 'updated_at']


class UploadTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadTask
        fields = [
            'task_name',
            'stage',
            'status',
            'payload',
            'result',
            'retry_count',
            'started_at',
            'finished_at',
            'created_at',
        ]


class UploadSessionSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    book_public_id = serializers.UUIDField(source='book.public_id', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    stages = IngestionStageRunSerializer(source='stage_runs', many=True, read_only=True)
    tasks = UploadTaskSerializer(many=True, read_only=True)

    class Meta:
        model = UploadSession
        fields = [
            'id',
            'public_id',
            'book',
            'book_public_id',
            'book_title',
            'initiated_by',
            'status',
            'current_stage',
            'source_note',
            'ai_pre_analysis',
            'confirmation_snapshot',
            'error_message',
            'stages',
            'tasks',
            'created_at',
            'updated_at',
        ]


class CreateIngestionJobSerializer(serializers.Serializer):
    book_public_id = serializers.UUIDField()
    source_note = serializers.CharField(required=False, allow_blank=True)

    def validate_book_public_id(self, value):
        user = self.context['request'].user
        try:
            return Book.objects.get(public_id=value, uploaded_by=user)
        except Book.DoesNotExist as exc:
            raise serializers.ValidationError('Book not found or not owned by the current user.') from exc

    def create(self, validated_data):
        book = validated_data['book_public_id']
        session = create_ingestion_job(
            book=book,
            initiated_by=self.context['request'].user,
        )
        session.source_note = validated_data.get('source_note', '')
        session.save(update_fields=['source_note', 'updated_at'])
        return session
