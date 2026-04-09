from rest_framework import serializers

from .models import SkillPack


class SkillPackSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    source_books = serializers.SerializerMethodField()

    class Meta:
        model = SkillPack
        fields = [
            'id',
            'public_id',
            'name',
            'subject',
            'sub_subject',
            'level',
            'source_books',
            'answer_template',
            'retrieval_rules',
            'citation_rules',
            'repeat_matan_policy',
            'summary_policy',
            'comparison_policy',
            'conflict_handling_policy',
            'scholar_priority_policy',
            'exercise_generation_policy',
            'language_style',
            'verification_requirements',
            'sensitivity_policy',
            'rules',
            'active',
            'review_status',
            'created_at',
        ]

    def get_source_books(self, obj):
        return [
            {
                'public_id': str(book.public_id),
                'title': book.title,
                'arabic_title': book.arabic_title,
            }
            for book in obj.source_books.all()
        ]
