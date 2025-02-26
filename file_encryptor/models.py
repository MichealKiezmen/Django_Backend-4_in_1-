from django.db import models
import uuid
from user.models import User

class FileEncryptModel(models.Model):
    file_id = models.CharField(primary_key=True, unique=True, default=uuid.uuid4, max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    encryption_key = models.TextField(unique=False)
    file_url = models.URLField(unique=False)
    file_extension = models.CharField(max_length=6, unique=False)

    def __str__(self):
        return f"{self.user.username}:{self.file_id} "
