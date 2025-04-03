from django.urls import path
from .views import Encryptor, Decryptor, EncryptionActionsView


urlpatterns = [
    path("encrypt/<int:user_id>/", Encryptor.as_view(), name="encrypt"),
    path("encrypt/actions/<str:data_id>/", EncryptionActionsView.as_view(), name="encrypt-actions"),
    path("decrypt/", Decryptor.as_view(), name="decrypt")
]
