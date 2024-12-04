from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import UserView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from cloud_app.serializers import UserSerializer
from rest_framework import status
import datetime



@api_view(['GET'])
def log_in(request, username, password):
    user_view = UserView()
    user = user_view.get_user(username=username)
    print(user.folder)

    if user and check_password(password, user.password):
        serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        print(f"[{datetime.datetime.now()}]info: User {username} logged in")
        response = Response({
            "message": "Login successful",
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
            "user": serializer.data
        },status=status.HTTP_200_OK)
        return response
    elif not user:
        print(f"[{datetime.datetime.now()}]error: Invalid username")
        response = Response({"message": "Invalid username"},status=status.HTTP_406_NOT_ACCEPTABLE)
        return response
    else:
        print(f"[{datetime.datetime.now()}]error: Invalid password")
        response = Response({"message": "Invalid password"},status=status.HTTP_406_NOT_ACCEPTABLE)
        return response
