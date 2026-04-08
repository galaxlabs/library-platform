from django.db import models
from apps.common.models import BaseModel

class Institute(BaseModel):
    name = models.CharField(max_length=255)
    admin = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True)
    policies = models.JSONField(default=dict)

class ClassDarjah(BaseModel):
    name = models.CharField(max_length=255)
    institute = models.ForeignKey(Institute, on_delete=models.CASCADE)
    level = models.IntegerField()

class Subject(BaseModel):
    name = models.CharField(max_length=255)
