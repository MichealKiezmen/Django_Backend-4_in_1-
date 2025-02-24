import datetime
import jwt
from django.conf import settings
from functools import wraps
from rest_framework.response import Response
from rest_framework import status



def create_access_token(verifierId: str) -> str:
    payload = dict(
        id=verifierId,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        iat=datetime.datetime.utcnow(),
    )

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token

def create_refresh_token(verifierId : str) -> str:
    payload = dict(
        id=verifierId,
        exp=datetime.datetime.utcnow() + datetime.timedelta(days=30),
        iat=datetime.datetime.utcnow(),
    )

    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")
    return token



def token_required(f):
    """A function that confirms if a user is authenticated or not"""
    @wraps(f)
    def decorated(*args, **kwargs):
        request = args[1]  # 'request' is the second argument (self, request)

        authorizationToken = request.headers.get('Authorization')

        if not authorizationToken: # Was a token sent?
            return Response({'message': 'Authorization token is missing'},
                            status=status.HTTP_401_UNAUTHORIZED)

        bToken = authorizationToken.split(" ")

        if len(bToken) < 2: # Was only "Bearer " sent?
            return Response({'message': 'Authorization token is missing'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            #Decode the token
            token = bToken[1]
            decoded_token  = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
            request.decoded_token = decoded_token
        except jwt.ExpiredSignatureError: #Has token expired?
            return Response({'message': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError: #Did the server generate the token?
            return Response({'message': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

        return f(*args, **kwargs)

    return decorated
