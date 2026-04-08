from django.db import models

from apps.common.models import BaseModel


class Book(BaseModel):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('institute', 'Institute'),
    ]
    REVIEW_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    arabic_title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    arabic_author_name = models.CharField(max_length=255, blank=True)
    compiler_editor = models.CharField(max_length=255, blank=True)
    translator = models.CharField(max_length=255, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    publication_year = models.CharField(max_length=20, blank=True)
    volume = models.CharField(max_length=50, blank=True)
    pages_count = models.PositiveIntegerField(null=True, blank=True)
    primary_subject = models.ForeignKey(
        'institutes.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='primary_books',
    )
    secondary_subjects = models.JSONField(default=list, blank=True)
    topic_tags = models.JSONField(default=list, blank=True)
    level = models.CharField(max_length=50, blank=True)
    audience = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=50, blank=True)
    related_sciences = models.JSONField(default=list, blank=True)
    madhhab = models.CharField(max_length=100, blank=True)
    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default='public',
    )
    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS_CHOICES,
        default='draft',
    )
    public = models.BooleanField(default=True)
    uploaded_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_books',
    )
    institute = models.ForeignKey(
        'institutes.Institute',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books',
    )
    source_origin = models.CharField(max_length=255, blank=True)
    copyright_license_note = models.TextField(blank=True)
    metadata_flags = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.arabic_title or self.title


class BookFile(BaseModel):
    FILE_KIND_CHOICES = [
        ('pdf', 'PDF'),
        ('image_bundle', 'Image Bundle'),
        ('text', 'Text'),
        ('epub', 'EPUB'),
        ('other', 'Other'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='books/')
    file_kind = models.CharField(max_length=30, choices=FILE_KIND_CHOICES, default='pdf')
    original_filename = models.CharField(max_length=255, blank=True)
    mime_type = models.CharField(max_length=100, blank=True)
    file_size_bytes = models.BigIntegerField(null=True, blank=True)
    checksum_sha256 = models.CharField(max_length=64, blank=True)
    scan_quality = models.CharField(max_length=50, blank=True)
    ocr_needed = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=True)


class BookMetadata(BaseModel):
    STATE_CHOICES = [
        ('user_entered', 'User Entered'),
        ('ai_detected', 'AI Detected'),
        ('reviewed', 'Reviewed'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='metadata_versions')
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    identity = models.JSONField(default=dict)
    classification = models.JSONField(default=dict)
    structure_hints = models.JSONField(default=dict)
    technical = models.JSONField(default=dict)
    review_notes = models.JSONField(default=dict)
    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='book_metadata_entries',
    )

    class Meta:
        unique_together = [('book', 'state')]


class BookStructureMap(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='structure_maps')
    version_label = models.CharField(max_length=100, blank=True)
    structure_data = models.JSONField(default=dict)
    heading_index = models.JSONField(default=list, blank=True)
    page_map = models.JSONField(default=list, blank=True)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


class BookTopicMap(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='topic_maps')
    topics = models.JSONField(default=list, blank=True)
    concept_links = models.JSONField(default=list, blank=True)
    graph_snapshot = models.JSONField(default=dict)


class BookChunk(BaseModel):
    CHUNK_TYPE_CHOICES = [
        ('paragraph', 'Paragraph'),
        ('question_answer', 'Question and Answer'),
        ('definition', 'Definition'),
        ('poem_bait', 'Poem Bait'),
        ('grammar_rule', 'Grammar Rule'),
        ('example', 'Example'),
        ('citation', 'Citation'),
        ('hadith', 'Hadith'),
        ('ayah', 'Ayah'),
        ('explanation', 'Explanation'),
        ('exercise', 'Exercise'),
        ('glossary_entry', 'Glossary Entry'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chunks')
    book_file = models.ForeignKey(
        BookFile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chunks',
    )
    chunk_type = models.CharField(max_length=30, choices=CHUNK_TYPE_CHOICES)
    page_number = models.PositiveIntegerField(null=True, blank=True)
    section_title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    normalized_content = models.TextField(blank=True)
    embedding_status = models.CharField(max_length=30, default='pending')
    metadata = models.JSONField(default=dict, blank=True)


class BookReference(BaseModel):
    RELATION_CHOICES = [
        ('matan', 'Matan'),
        ('sharh', 'Sharh'),
        ('hashiyah', 'Hashiyah'),
        ('translation', 'Translation'),
        ('commentary', 'Commentary'),
        ('summary', 'Summary'),
        ('approved_edition', 'Institute Approved Edition'),
    ]

    source_book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='outgoing_references',
    )
    target_book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='incoming_references',
    )
    relation_type = models.CharField(max_length=30, choices=RELATION_CHOICES)
    notes = models.TextField(blank=True)


class BookApprovalReview(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('needs_changes', 'Needs Changes'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='approval_reviews')
    reviewer = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='book_reviews',
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    comments = models.TextField(blank=True)
    decision_metadata = models.JSONField(default=dict, blank=True)
