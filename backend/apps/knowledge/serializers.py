from rest_framework import serializers

from .models import KnowledgeObject


class KnowledgeObjectSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)

    class Meta:
        model = KnowledgeObject
        fields = [
            'id',
            'public_id',
            'book',
            'book_title',
            'chunk',
            'skill_pack',
            'subject',
            'subject_name',
            'object_type',
            'title',
            'topic',
            'content',
            'data',
            'is_published',
            'created_at',
        ]
