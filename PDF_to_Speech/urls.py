from django.urls import path
from .views import PDF_To_TextAPI

urlpatterns = [
    path("", PDF_To_TextAPI.as_view() ,name="home_pdf_to_speech"),
]
