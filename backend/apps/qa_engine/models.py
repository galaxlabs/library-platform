from django.db import models

from apps.common.models import BaseModel


class Query(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    question = models.TextField()
    language_pair = models.CharField(max_length=50, default='ar-en')
    detected_subject = models.CharField(max_length=255, blank=True)
    detected_sub_subject = models.CharField(max_length=255, blank=True)
    detected_intent = models.CharField(max_length=255, blank=True)
    detected_level = models.CharField(max_length=100, blank=True)
    sensitivity_level = models.CharField(max_length=50, default='normal')
    search_scope = models.CharField(max_length=50, default='general')
    verification_preference = models.CharField(max_length=50, default='default')
    response = models.JSONField(default=dict)


class Answer(BaseModel):
    VERIFICATION_CHOICES = [
        ('source_grounded', 'Source Grounded'),
        ('scholar_verified', 'Scholar Verified'),
        ('disputed', 'Disputed'),
        ('ai_summary_only', 'AI Summary Only'),
        ('needs_review', 'Needs Review'),
    ]

    query = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='answers')
    selected_skill_pack = models.ForeignKey(
        'skills.SkillPack',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='answers',
    )
    raw_engine_output = models.JSONField(default=dict, blank=True)
    direct_answer = models.TextField(blank=True)
    detailed_explanation = models.TextField(blank=True)
    simplified_explanation = models.TextField(blank=True)
    generated_examples = models.JSONField(default=list, blank=True)
    optional_exercises = models.JSONField(default=list, blank=True)
    scholar_reviews_snapshot = models.JSONField(default=list, blank=True)
    verification_status = models.CharField(
        max_length=30,
        choices=VERIFICATION_CHOICES,
        default='needs_review',
    )
    confidence = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    related_topics = models.JSONField(default=list, blank=True)
    answer_provenance = models.JSONField(default=dict, blank=True)


class RetrievedSource(BaseModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='retrieved_sources')
    book = models.ForeignKey(
        'library.Book',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='retrieval_hits',
    )
    chunk = models.ForeignKey(
        'library.BookChunk',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='retrieval_hits',
    )
    page_number = models.PositiveIntegerField(null=True, blank=True)
    score = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    retrieval_reason = models.CharField(max_length=255, blank=True)


class QuotedPassage(BaseModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='quoted_passages')
    source = models.ForeignKey(
        RetrievedSource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='quoted_passages',
    )
    quoted_text = models.TextField()
    snippet = models.TextField(blank=True)
