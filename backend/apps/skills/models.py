from django.db import models

from apps.common.models import BaseModel


class SkillPack(BaseModel):
    REVIEW_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    sub_subject = models.CharField(max_length=255, blank=True)
    level = models.CharField(max_length=50, blank=True)
    source_books = models.ManyToManyField(
        'library.Book',
        related_name='skill_packs',
        blank=True,
    )
    answer_template = models.JSONField(default=dict, blank=True)
    retrieval_rules = models.JSONField(default=dict, blank=True)
    citation_rules = models.JSONField(default=dict, blank=True)
    repeat_matan_policy = models.JSONField(default=dict, blank=True)
    summary_policy = models.JSONField(default=dict, blank=True)
    comparison_policy = models.JSONField(default=dict, blank=True)
    conflict_handling_policy = models.JSONField(default=dict, blank=True)
    scholar_priority_policy = models.JSONField(default=dict, blank=True)
    exercise_generation_policy = models.JSONField(default=dict, blank=True)
    language_style = models.JSONField(default=dict, blank=True)
    verification_requirements = models.JSONField(default=dict, blank=True)
    sensitivity_policy = models.JSONField(default=dict, blank=True)
    rules = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)
    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS_CHOICES,
        default='draft',
    )

    def __str__(self):
        return self.name
