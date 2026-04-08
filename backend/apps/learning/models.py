from django.db import models

from apps.common.models import BaseModel


class Exercise(BaseModel):
    type = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    subject = models.CharField(max_length=255, blank=True)
    prompt = models.TextField(blank=True)
    answer_key = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class PracticeAttempt(BaseModel):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='practice_attempts')
    response = models.JSONField(default=dict, blank=True)
    is_correct = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)


class WeakTopic(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='weak_topics')
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    confidence = models.DecimalField(max_digits=5, decimal_places=2, default=0)


class RevisionList(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='revision_lists')
    title = models.CharField(max_length=255)
    items = models.JSONField(default=list, blank=True)


class Bookmark(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='bookmarks')
    book = models.ForeignKey(
        'library.Book',
        on_delete=models.CASCADE,
        related_name='bookmarks',
        null=True,
        blank=True,
    )
    answer = models.ForeignKey(
        'qa_engine.Answer',
        on_delete=models.CASCADE,
        related_name='bookmarks',
        null=True,
        blank=True,
    )
    note = models.TextField(blank=True)
