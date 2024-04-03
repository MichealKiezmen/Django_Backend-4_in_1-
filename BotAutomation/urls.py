from django.urls import path
from .views import UploadVideo

urlpatterns = [
    path("upload_video",UploadVideo.as_view() ,name="upload_video"),
]
