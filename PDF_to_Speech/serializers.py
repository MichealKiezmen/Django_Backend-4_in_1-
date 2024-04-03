from rest_framework import serializers
from .models import AudioModel

class AudioDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = AudioModel
        fields = '__all__'
