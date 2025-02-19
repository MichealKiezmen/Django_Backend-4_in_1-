from django.urls import path
from .views import UserAPI

urlpatterns = [
    path("login/", UserAPI.as_view(), name="user-login" )
]