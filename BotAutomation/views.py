from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .rccg_bot import RccgSol


# Create your views here.
class UploadVideo(APIView):

    def get(self, request):
        pass


    def post(self, request):
        programs = {
        "thursday": 1,
        "sunday": 2,
        "daily": 3,
        "others": 4
         }

        youtuber = request.data["youtuber"]
        category = request.data["category"]
        theme = request.data["theme"]
        date = request.data["date"]

        bot = RccgSol()
        startYTbot = bot.open_youtube(youtuber)
        if startYTbot:
            start_rccg = bot.open_rccg_sol(theme,programs[category],date)

        return Response({
            "message": "Automation Suceessful."
        }, status=status.HTTP_200_OK)
