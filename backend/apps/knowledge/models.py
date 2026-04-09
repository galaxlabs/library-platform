from django.db import models

from apps.common.models import BaseModel


class KnowledgeObject(BaseModel):
    OBJECT_CHOICES = [
        ('topic', 'Topic'),
        ('concept', 'Concept'),
        ('rule', 'Rule'),
        ('example', 'Example'),
        ('definition', 'Definition'),
    ]

    book = models.ForeignKey(
        'library.Book',
        on_delete=models.CASCADE,
        related_name='knowledge_objects',
        null=True,
        blank=True,
    )
    chunk = models.ForeignKey(
        'library.BookChunk',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='knowledge_objects',
    )
    skill_pack = models.ForeignKey(
        'skills.SkillPack',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='knowledge_objects',
    )
    subject = models.ForeignKey(
        'institutes.Subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='knowledge_objects',
    )
    object_type = models.CharField(max_length=30, choices=OBJECT_CHOICES)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
