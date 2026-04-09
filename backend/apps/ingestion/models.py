from django.db import models

from apps.common.models import BaseModel


class UploadSession(BaseModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('uploaded', 'Uploaded'),
        ('metadata_pending', 'Metadata Pending'),
        ('queued', 'Queued'),
        ('processing', 'Processing'),
        ('review_pending', 'Review Pending'),
        ('published', 'Published'),
        ('failed', 'Failed'),
    ]

    book = models.ForeignKey(
        'library.Book',
        on_delete=models.CASCADE,
        related_name='upload_sessions',
        null=True,
        blank=True,
    )
    initiated_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='upload_sessions',
    )
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    current_stage = models.CharField(max_length=50, default='file_saved')
    source_note = models.TextField(blank=True)
    ai_pre_analysis = models.JSONField(default=dict, blank=True)
    confirmation_snapshot = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)


class UploadTask(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    upload_session = models.ForeignKey(
        UploadSession,
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True,
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    task_name = models.CharField(max_length=100, blank=True)
    stage = models.CharField(max_length=50, blank=True)
    payload = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    retry_count = models.PositiveIntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)


class IngestionStageRun(BaseModel):
    STAGE_CHOICES = [
        ('file_saved', 'File Saved'),
        ('ocr_detection', 'OCR Detection'),
        ('page_extraction', 'Page Extraction'),
        ('arabic_normalization', 'Arabic Normalization'),
        ('page_mapping', 'Page Mapping'),
        ('heading_detection', 'Heading Detection'),
        ('chunking', 'Chunking'),
        ('embedding_generation', 'Embedding Generation'),
        ('concept_extraction', 'Concept Extraction'),
        ('topic_graph_generation', 'Topic Graph Generation'),
        ('skill_pack_draft_generation', 'Skill Pack Draft Generation'),
        ('review', 'Review'),
        ('publish', 'Publish'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('skipped', 'Skipped'),
    ]

    upload_session = models.ForeignKey(
        UploadSession,
        on_delete=models.CASCADE,
        related_name='stage_runs',
    )
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    diagnostics = models.JSONField(default=dict, blank=True)
    operator_notes = models.TextField(blank=True)
