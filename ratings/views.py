from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import os
from dotenv import load_dotenv


load_dotenv(override=True)


READ_ACCESS_TOKEN = os.getenv("READ_ACCESS_TOKEN")

class MoviesRatings(APIView):
    
    def get(self, request, movie_name, category):
        url = f"https://api.themoviedb.org/3/search/{category}?query={movie_name}"
        headers = {
            "Authorization": f"Bearer {READ_ACCESS_TOKEN}"
        }
        try:
            response = requests.get(url, headers=headers).json()
            if response:
                top5 =response["results"][:5]
            
                return Response(top5, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        pass