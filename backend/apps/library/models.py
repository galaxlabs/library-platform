from django.db import models
from apps.common.models import BaseModel

class Book(BaseModel):
    title = models.CharField(max_length=255)
    arabic_title = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, blank=True)
    public = models.BooleanField(default=True)
