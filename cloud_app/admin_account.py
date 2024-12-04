from rest_framework.decorators import api_view
from rest_framework.response import Response
from auth_app.views import UserView
from .views import FileView
from django.http import HttpResponse
import mimetypes
from .serializers import FileSerializer, UserSerializer
import os, datetime, re
from rest_framework_simplejwt.tokens import RefreshToken
from auth_app.views import UserView
from rest_framework import status
from .is_admin_decorator import is_admin
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password



@api_view(['POST'])
@is_admin
def admin_create_user(request):
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
        refresh = RefreshToken.for_user(new_user)
        print(f"[{datetime.datetime.now()}]info: User {new_user.username} registrated")
        return Response({
            "message": "Login successful",
            "refresh_token": str(refresh),
            "access_token": str(refresh.access_token),
        },status=status.HTTP_201_CREATED)
    else:
        print(f"[{datetime.datetime.now()}]error: Server-side error during registration")
        return Response({"message":"Server-side error repeat again"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@is_admin
def admin_get_all_users(request, user_id):
    user_view = UserView()
    users = user_view.get_all_users()
    if users is not None:
        serializer = UserSerializer(users, many=True)
        print(f"[{datetime.datetime.now()}]info: Admin get all users")
        return Response({"users":serializer.data}, status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: Filed get all users by admin")
    return Response({"message":'Users not found'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@is_admin
def admin_change_permissions(request, user_id):
    user_view = UserView()
    if user_view.change_premissions(user_id=user_id):
        print(f"[{datetime.datetime.now()}]info: Admin change permission user {user_id}")
        return Response({"message":'Permissions user {user_id} changed successfully'},status=status.HTTP_200_OK)
    else:
        print(f"[{datetime.datetime.now()}]error: Failed chnage permission user {user_id} by admin")
        return Response({'message': 'Filed change permissions'},status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['DELETE'])
@is_admin
def admin_delete_user(request,user_id):
    if UserView.delete_user(request,user_id):
        print(f"[{datetime.datetime.now()}]info: Admin delete user {user_id}")
        return Response({"message":"User deleted successfully"},status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: Failed delete user {user_id} by admin")
    return Response({"message":"User wasn't delete"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@is_admin
def admin_upload_file(request,user_id):
    if not request.FILES['file']:
        print(f"[{datetime.datetime.now()}]error: Admin not sent file for user {user_id}")
        return Response({"message":" File not sent"},status=status.HTTP_403_FORBIDDEN)
    else:           
        file = request.FILES['file']
        description = request.data['description'] if request.data['description'] else None
        new_file = FileView()
        if new_file.add_file(user_id=user_id,file=file,description=description):
            print(f"[{datetime.datetime.now()}]info: File {file.name} uploaded")
            return Response({"message":"File upload successfully"},status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: Failed upload file by admin to user {user_id}")
    return Response({"message":"File upload failed"},status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@is_admin
def admin_get_all_user_files(request,user_id):
    print("Ghbdtn",request, user_id)
    file_view = FileView()
    print(user_id)
    all_files = file_view.get_all_user_files(user_id=user_id)
    if all_files:
        serializer = FileSerializer(all_files, many=True)
        print(f"[{datetime.datetime.now()}]info: Files {user_id} sended to admin")
        return Response({"files": serializer.data},status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: Admin don't get all files user {user_id}")
    return Response({"message":"Failed to retrieve files try again"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@is_admin
def admin_get_file_by_id(request,user_id,file_id):
    file_view = FileView()
    file = file_view.get_file(file_id=file_id)
    
    file_path = os.path.join(f'../cloud_store/{file.user.id}', file.name)

    if file:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as result:
                response = HttpResponse(result.read(), content_type=mimetypes.guess_type(file_path)[0])
                response['Content-Disposition'] = f'attachment; filename="{file.name}"'
                print(f"[{datetime.datetime.now()}]info: file {file.id} sended to admin")
                return response
    
    print(f"[{datetime.datetime.now()}]error: Admin not get file {file_id}")
    return Response({"message":"Failed to retrive your file try again"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@is_admin
def admin_get_file_link(request,user_id,file_id):
    file_view = FileView()
    link = file_view.get_file_link(file_id=file_id)
    if link:
        print(f"[{datetime.datetime.now()}]info: Admin create link for file {file_id}")
        return Response({"link": link},status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: Failed creating link for file {file_id} by admin")
    return Response({"message":"Failed to get file link try again"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@is_admin
def admin_delete_file(request,user_id,file_id):
    file_view = FileView()
    if file_view.delete_file(file_id=file_id):
        print(f"[{datetime.datetime.now()}]info: Admin delete file {file_id}")
        return Response({"message":"File deleted successfully"},status=status.HTTP_200_OK)

    print(f"[{datetime.datetime.now()}]error: Failed delete file {file_id} by admin")
    return Response({"message":"File wasn't delete"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@is_admin
def admin_update_file(request,user_id,file_id):
    file_view = FileView()
    data = request.data
    file = file_view.change_file(file_id=file_id, data=data)
    if file:
        print(f"[{datetime.datetime.now()}]info: User {user_id} change description file {file_id}")
        return Response({"message":"File updated successfully"}, status=status.HTTP_200_OK)           
    
    print(f"[{datetime.datetime.now()}]error: File {file_id} not updated by user {user_id}")
    return Response({"message":"File not updated"},status=status.HTTP_403_FORBIDDEN)  



    
