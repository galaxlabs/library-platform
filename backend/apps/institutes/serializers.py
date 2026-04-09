from rest_framework import serializers

from .models import (
    ClassDarjah,
    Institute,
    InstituteMembership,
    InstitutePrivateLibraryAccess,
    InstituteSubject,
    Subject,
)


class SubjectSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id',
            'public_id',
            'name',
            'slug',
            'arabic_name',
            'description',
        ]


class ClassDarjahSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    institute_name = serializers.CharField(source='institute.name', read_only=True)

    class Meta:
        model = ClassDarjah
        fields = [
            'id',
            'public_id',
            'name',
            'code',
            'institute',
            'institute_name',
            'level',
            'order_index',
            'language_pair',
            'metadata',
        ]


class InstituteMembershipSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_full_name = serializers.CharField(source='user.full_name', read_only=True)
    institute_name = serializers.CharField(source='institute.name', read_only=True)
    class_darjah_name = serializers.CharField(source='class_darjah.name', read_only=True)

    class Meta:
        model = InstituteMembership
        fields = [
            'id',
            'public_id',
            'user',
            'user_email',
            'user_full_name',
            'institute',
            'institute_name',
            'class_darjah',
            'class_darjah_name',
            'role',
            'is_active',
            'joined_at',
        ]
        read_only_fields = ['joined_at']


class InstituteSubjectSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    subject_detail = SubjectSerializer(source='subject', read_only=True)
    class_darjah_name = serializers.CharField(source='class_darjah.name', read_only=True)

    class Meta:
        model = InstituteSubject
        fields = [
            'id',
            'public_id',
            'institute',
            'subject',
            'subject_detail',
            'class_darjah',
            'class_darjah_name',
            'curriculum_metadata',
            'is_required',
        ]


class InstitutePrivateLibraryAccessSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = InstitutePrivateLibraryAccess
        fields = [
            'id',
            'public_id',
            'institute',
            'book',
            'book_title',
            'access_level',
            'is_active',
        ]


class InstituteSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    classes = ClassDarjahSerializer(many=True, read_only=True)
    subject_offerings = InstituteSubjectSerializer(many=True, read_only=True)
    memberships_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Institute
        fields = [
            'id',
            'public_id',
            'name',
            'slug',
            'description',
            'country',
            'city',
            'contact_email',
            'is_active',
            'admin',
            'policies',
            'branding',
            'memberships_count',
            'classes',
            'subject_offerings',
        ]
