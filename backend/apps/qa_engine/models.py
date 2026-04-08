from django.db import models
from apps.common.models import BaseModel

class Query(BaseModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    question = models.TextField()
    response = models.JSONField(default=dict)
