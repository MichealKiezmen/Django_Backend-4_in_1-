from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=250)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verifierId = models.CharField(max_length=250)
    profile_picture = models.TextField(null=True, blank=True)
    refresh_token = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.username} ID:{self.verifierId}"
