from django.db import models
from django.utils.timezone import now


class BaseModel(models.Model):
    """
    Abstract base model for all app models.
    Provides common fields: created_at, updated_at.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']