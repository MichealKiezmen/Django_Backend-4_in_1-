from django.db import models
import uuid
from user.models import User

class FileEncryptModel(models.Model):
    file_id = models.CharField(primary_key=True, default=uuid.uuid4(), max_length=70)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    encryption_key = models.TextField(unique=False)
    file_url = models.URLField(unique=False)
    file_extension = models.CharField(max_length=6, unique=False)