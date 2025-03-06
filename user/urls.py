from django.urls import path
from .views import LoginUser, AuthMe, TokenRefresh

urlpatterns = [
    path("login/", LoginUser.as_view(), name="user-login"),
    path("me/", AuthMe.as_view(), name="user-data"),
    path("refresh/", TokenRefresh.as_view(), name="token-refresh")
]
