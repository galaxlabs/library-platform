from django.db import models

class Metric(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()
