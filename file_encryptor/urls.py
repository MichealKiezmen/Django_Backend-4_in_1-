from django.urls import path
from .views import Encryptor, Decryptor


urlpatterns = [
    path("encrypt/<int:user_id>/", Encryptor.as_view(), name="encrypt"),
    path("decrypt/", Decryptor.as_view(), name="decrypt")
]