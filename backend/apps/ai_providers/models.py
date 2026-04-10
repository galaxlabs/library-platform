import os

from cryptography.fernet import Fernet, InvalidToken
from django.db import models

from apps.common.models import BaseModel


class AIProvider(BaseModel):
    PROVIDER_CHOICES = [
        ('gemini', 'Google Gemini'),
        ('openrouter', 'OpenRouter'),
        ('ollama', 'Ollama (Local)'),
    ]

    SCOPE_CHOICES = [
        ('system', 'System Default'),
        ('institute', 'Institute Level'),
        ('user', 'User Personal'),
    ]

    name = models.CharField(max_length=50, choices=PROVIDER_CHOICES)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='system')
    api_key = models.TextField(blank=True, default='')
    base_url = models.URLField(null=True, blank=True)
    model_name = models.CharField(max_length=100, null=True, blank=True)
    institute = models.ForeignKey(
        'institutes.Institute',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ai_providers',
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ai_providers',
    )
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0)
    rate_limit = models.IntegerField(default=0)
    timeout_seconds = models.IntegerField(default=30)
    config = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = [('name', 'scope', 'institute', 'user')]
        ordering = ['-priority', 'name']

    def __str__(self):
        return f'{self.get_name_display()} ({self.get_scope_display()})'

    def decrypt_key(self):
        if not self.api_key:
            return ''
        encryption_key = os.getenv('ENCRYPTION_KEY')
        if not encryption_key:
            return self.api_key
        try:
            cipher_suite = Fernet(encryption_key.encode())
            return cipher_suite.decrypt(self.api_key.encode()).decode()
        except (InvalidToken, ValueError, TypeError):
            return self.api_key

    def encrypt_key(self, key):
        encryption_key = os.getenv('ENCRYPTION_KEY')
        if not encryption_key:
            self.api_key = key
            return
        try:
            cipher_suite = Fernet(encryption_key.encode())
            self.api_key = cipher_suite.encrypt(key.encode()).decode()
        except (ValueError, TypeError):
            self.api_key = key
