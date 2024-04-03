from django.db import models

# Create your models here.
class AudioModel(models.Model):
    url = models.CharField(max_length=250)
