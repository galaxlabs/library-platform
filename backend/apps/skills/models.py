from django.db import models
from apps.common.models import BaseModel

class SkillPack(BaseModel):
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    rules = models.JSONField(default=dict)
    active = models.BooleanField(default=True)
