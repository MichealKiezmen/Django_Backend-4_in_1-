from django.urls import path
from .views import MoviesRatings

urlpatterns = [
    path("movie-rating/<movie_name>/<category>/", MoviesRatings.as_view(), name="movie-rating")
]