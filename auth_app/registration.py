from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import UserView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework import status
import re, datetime
from cloud_app.serializers import UserSerializer

@api_view(['POST'])
def registration(request):
    data = request.data
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', data['username']):
        print(f"[{datetime.datetime.now()}]error: Username incorrect")
        return Response({"message":"Username must contain only English letters and numbers"},status=status.HTTP_406_NOT_ACCEPTABLE)
    elif not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{6,}$', data['password']):
        print(f"[{datetime.datetime.now()}]error: Password incorrect")
        return Response({"message":"The password must be at least 6 characters: at least one capital letter, one number and one special character"},status=status.HTTP_406_NOT_ACCEPTABLE)
    elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', data['email']):
        print(f"[{datetime.datetime.now()}]error: Email incorrect")
        return Response({"message":"Email does not match the format of email addresses"},status=status.HTTP_406_NOT_ACCEPTABLE)
    data['password'] = make_password(data['password'])
    user_view = UserView()
    new_user = user_view.create_user(data=data)
    if new_user:
        serializer = UserSerializer(new_user)
        refresh = RefreshToken.for_user(new_user)
        print(f"[{datetime.datetime.now()}]info: User {new_user.username} registrated")
        return Response({
            "message": "Login successful",
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "user": serializer.data
        },status=status.HTTP_201_CREATED)
    else:
        print(f"[{datetime.datetime.now()}]error: Server-side error during registration")
        return Response({"message":"Server-side error repeat again"},status=status.HTTP_400_BAD_REQUEST)