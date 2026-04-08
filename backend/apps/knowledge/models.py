from django.db import models

class KnowledgeObject(models.Model):
    type = models.CharField(max_length=50)
    data = models.JSONField(default=dict)
