from django.urls import path
from .views import UserAPI, LoginUser

urlpatterns = [
    path("me/", UserAPI.as_view(), name="user-data" ),
    path("login/", LoginUser.as_view(), name="user-login")
]
