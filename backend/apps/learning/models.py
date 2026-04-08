from django.db import models

class Exercise(models.Model):
    type = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
