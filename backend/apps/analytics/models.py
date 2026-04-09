from django.db import models

from apps.common.models import BaseModel


class Metric(BaseModel):
    name = models.CharField(max_length=255)
    value = models.FloatField(default=0)
    scope = models.CharField(max_length=50, default='system')
    metadata = models.JSONField(default=dict, blank=True)


class EventLog(BaseModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analytics_events',
    )
    payload = models.JSONField(default=dict, blank=True)
