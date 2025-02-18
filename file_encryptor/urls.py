from django.urls import path
from .views import Encryptor


urlpatterns = [
    path("encrypt/", Encryptor.as_view(), name="encrypt"),
]