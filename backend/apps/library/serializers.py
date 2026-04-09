from rest_framework import serializers

from apps.institutes.models import InstitutePrivateLibraryAccess

from .models import Book, BookChunk, BookFile, BookMetadata, BookReference


class BookFileSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = BookFile
        fields = [
            'id',
            'public_id',
            'file',
            'file_kind',
            'original_filename',
            'mime_type',
            'file_size_bytes',
            'checksum_sha256',
            'scan_quality',
            'ocr_needed',
            'is_primary',
        ]


class BookChunkSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = BookChunk
        fields = [
            'id',
            'public_id',
            'chunk_type',
            'page_number',
            'section_title',
            'content',
            'normalized_content',
            'embedding_status',
            'metadata',
        ]


class BookReferenceSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    source_book_title = serializers.CharField(source='source_book.title', read_only=True)
    target_book_title = serializers.CharField(source='target_book.title', read_only=True)

    class Meta:
        model = BookReference
        fields = [
            'id',
            'public_id',
            'source_book',
            'source_book_title',
            'target_book',
            'target_book_title',
            'relation_type',
            'notes',
        ]


class BookMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMetadata
        fields = [
            'state',
            'identity',
            'classification',
            'structure_hints',
            'technical',
            'review_notes',
        ]


class BookListSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    primary_subject_name = serializers.CharField(source='primary_subject.name', read_only=True)
    files_count = serializers.IntegerField(read_only=True)
    chunks_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'public_id',
            'title',
            'arabic_title',
            'author',
            'arabic_author_name',
            'primary_subject',
            'primary_subject_name',
            'level',
            'language',
            'visibility',
            'review_status',
            'public',
            'files_count',
            'chunks_count',
            'created_at',
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    public_id = serializers.UUIDField(read_only=True)
    files = BookFileSerializer(many=True, read_only=True)
    latest_metadata = serializers.SerializerMethodField()
    primary_subject_name = serializers.CharField(source='primary_subject.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'public_id',
            'title',
            'arabic_title',
            'author',
            'arabic_author_name',
            'compiler_editor',
            'translator',
            'publisher',
            'edition',
            'publication_year',
            'volume',
            'pages_count',
            'primary_subject',
            'primary_subject_name',
            'secondary_subjects',
            'topic_tags',
            'level',
            'audience',
            'language',
            'related_sciences',
            'madhhab',
            'visibility',
            'review_status',
            'public',
            'uploaded_by',
            'institute',
            'source_origin',
            'copyright_license_note',
            'metadata_flags',
            'files',
            'latest_metadata',
            'created_at',
        ]

    def get_latest_metadata(self, obj):
        metadata = obj.metadata_versions.order_by('-created_at').first()
        if not metadata:
            return None
        return BookMetadataSerializer(metadata).data


class BookCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    file_kind = serializers.ChoiceField(choices=BookFile.FILE_KIND_CHOICES, default='pdf')
    subject = serializers.PrimaryKeyRelatedField(
        source='primary_subject',
        queryset=Book._meta.get_field('primary_subject').remote_field.model.objects.all(),
        required=False,
        allow_null=True,
    )
    metadata_identity = serializers.JSONField(write_only=True, required=False, default=dict)
    metadata_classification = serializers.JSONField(write_only=True, required=False, default=dict)
    metadata_structure_hints = serializers.JSONField(write_only=True, required=False, default=dict)

    class Meta:
        model = Book
        fields = [
            'title',
            'arabic_title',
            'author',
            'arabic_author_name',
            'compiler_editor',
            'translator',
            'publisher',
            'edition',
            'publication_year',
            'volume',
            'pages_count',
            'subject',
            'secondary_subjects',
            'topic_tags',
            'level',
            'audience',
            'language',
            'related_sciences',
            'madhhab',
            'visibility',
            'public',
            'institute',
            'source_origin',
            'copyright_license_note',
            'metadata_flags',
            'file',
            'file_kind',
            'metadata_identity',
            'metadata_classification',
            'metadata_structure_hints',
        ]

    def validate(self, attrs):
        request = self.context['request']
        visibility = attrs.get('visibility', 'public')
        institute = attrs.get('institute')
        if visibility in {'private', 'institute'} and not institute and getattr(request.user, 'institute', None):
            attrs['institute'] = request.user.institute
        if visibility == 'institute' and not attrs.get('institute'):
            raise serializers.ValidationError({'institute': 'Institute visibility requires an institute.'})
        return attrs

    def create(self, validated_data):
        upload = validated_data.pop('file')
        file_kind = validated_data.pop('file_kind', 'pdf')
        metadata_identity = validated_data.pop('metadata_identity', {})
        metadata_classification = validated_data.pop('metadata_classification', {})
        metadata_structure_hints = validated_data.pop('metadata_structure_hints', {})
        request = self.context['request']

        book = Book.objects.create(
            uploaded_by=request.user,
            review_status='draft',
            **validated_data,
        )
        BookFile.objects.create(
            book=book,
            file=upload,
            file_kind=file_kind,
            original_filename=getattr(upload, 'name', ''),
            mime_type=getattr(upload, 'content_type', ''),
            file_size_bytes=getattr(upload, 'size', None),
            is_primary=True,
            ocr_needed=file_kind == 'pdf',
        )
        BookMetadata.objects.create(
            book=book,
            state='user_entered',
            identity=metadata_identity or {
                'title': book.title,
                'arabic_title': book.arabic_title,
                'author': book.author,
            },
            classification=metadata_classification or {
                'primary_subject_id': book.primary_subject_id,
                'level': book.level,
                'language': book.language,
            },
            structure_hints=metadata_structure_hints,
            created_by=request.user,
        )
        if book.visibility == 'institute' and book.institute_id:
            InstitutePrivateLibraryAccess.objects.get_or_create(
                institute=book.institute,
                book=book,
                defaults={'access_level': 'study', 'is_active': True},
            )
        return book
