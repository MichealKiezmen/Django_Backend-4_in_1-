from django.db import models
import uuid
from datetime import datetime
from user.models import User

class FileEncryptModel(models.Model):
    file_id = models.CharField(primary_key=True, unique=True,
                               default=f"{str(datetime.today().isoformat())}-{uuid.uuid4()}",
                               max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    encryption_key = models.TextField(unique=False)
    google_drive_file_id = models.CharField(max_length=200)
    file_url = models.URLField(unique=False)
    file_name = models.CharField(max_length=150, unique=False)
    file_extension = models.CharField(max_length=6, unique=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}:{self.file_name} "
