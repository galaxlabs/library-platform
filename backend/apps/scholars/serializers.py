from rest_framework import serializers

from apps.qa_engine.models import Answer

from .models import Scholar, ScholarCredential, ScholarReview


class ScholarCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarCredential
        fields = ['id', 'credential_type', 'title', 'issuing_body', 'document', 'metadata']


class ScholarSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    credentials = ScholarCredentialSerializer(many=True, read_only=True)

    class Meta:
        model = Scholar
        fields = [
            'id',
            'public_id',
            'user',
            'full_name',
            'arabic_name',
            'phone',
            'country',
            'city',
            'madrasa_or_institute',
            'darjah_or_final_year',
            'sanad_or_ijazah_info',
            'specialization',
            'specialization_subjects',
            'current_teaching_role',
            'short_bio',
            'profile_photo',
            'admin_notes',
            'verification_status',
            'badge_status',
            'trust_score',
            'review_count',
            'correction_count',
            'credentials',
            'created_at',
        ]
        read_only_fields = ['verification_status', 'badge_status', 'trust_score', 'review_count', 'correction_count']


class ScholarApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholar
        exclude = ['admin_notes', 'badge_status', 'trust_score', 'review_count', 'correction_count', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        scholar, _ = Scholar.objects.update_or_create(
            user=user,
            defaults={
                **validated_data,
                'verification_status': 'under_review',
                'full_name': validated_data.get('full_name') or user.full_name,
                'arabic_name': validated_data.get('arabic_name') or user.arabic_name,
            },
        )
        return scholar


class ScholarReviewSerializer(serializers.ModelSerializer):
    answer_public_id = serializers.UUIDField(write_only=True, required=True)
    scholar_name = serializers.CharField(source='scholar.full_name', read_only=True)
    answer_question = serializers.CharField(source='answer.query.question', read_only=True)

    class Meta:
        model = ScholarReview
        fields = [
            'id',
            'answer_public_id',
            'scholar',
            'scholar_name',
            'answer',
            'answer_question',
            'decision',
            'commentary',
            'evidence_notes',
            'created_at',
        ]
        read_only_fields = ['scholar', 'answer']

    def create(self, validated_data):
        answer_public_id = validated_data.pop('answer_public_id')
        answer = Answer.objects.get(public_id=answer_public_id)
        scholar = self.context['request'].user.scholar_profile
        review = ScholarReview.objects.create(
            scholar=scholar,
            answer=answer,
            **validated_data,
        )
        scholar.review_count = scholar.reviews.count()
        scholar.save(update_fields=['review_count', 'updated_at'])
        return review
