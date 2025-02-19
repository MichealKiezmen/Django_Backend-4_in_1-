from rest_framework.serializers import ModelSerializer
from .models import FileEncryptModel

class FileEncryptModelSerializer(ModelSerializer):
    class Meta:
        model = FileEncryptModel
        fields = "__all__"
