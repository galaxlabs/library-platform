from django.db import models
from apps.common.models import BaseModel

class Scholar(BaseModel):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255, blank=True)
    verification_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ])
