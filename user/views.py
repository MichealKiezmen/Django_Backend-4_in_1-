from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from .services import create_access_token, create_refresh_token, token_required

class UserAPI(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

class LoginUser(APIView):

    def post(self, request):
        body = request.data
        id = request.data["verifierId"]

        access_token = create_access_token(verifierId=id)
        refresh_token = create_refresh_token(verifierId=id)

        #Find User
        try:
            existing_user = User.objects.get(verifierId=id)
            if existing_user:
                existing_user.refresh_token = refresh_token
                existing_user.save()

                return Response({"data": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "new_user": "False"
                        }},  status=status.HTTP_200_OK)
        except User.DoesNotExist:
            body["refresh_token"] = refresh_token
            serializer = UserSerializer(data=body)
            if serializer.is_valid():
                serializer.save()
                return Response({"data": {
                         "access_token": access_token,
                        "refresh_token": refresh_token,
                        "new_user": "True"
                    }},  status=status.HTTP_201_CREATED)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
