from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from auth_app.views import UserView
from .views import FileView
from .serializers import UserSerializer
from django.http import HttpResponse
import mimetypes
from .serializers import FileSerializer
from .jwt_user_id_decorator import jwt_user_id_compare
import os, datetime
from transliterate import translit


@api_view(['DELETE'])
@jwt_user_id_compare
def delete_user(request,user_id):
    if UserView.delete_user(request,user_id):
        print(f"[{datetime.datetime.now()}]info: User {user_id} deleted")
        return Response({"message":"User deleted successfully"},status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: User {user_id} not deleted")
    return Response({"message":"User wasn't delete"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@jwt_user_id_compare
def update_user(request, user_id):
    user_view = UserView()
    user = user_view.update_user(user_id=user_id,data=request.data)

    if user:
        serializer = UserSerializer(user)    
        print(f"[{datetime.datetime.now()}]info: User {user_id} changed")
        return Response({"message":"User updated successfully", "user":serializer.data},status=status.HTTP_200_OK)
    else:
        print(f"[{datetime.datetime.now()}]error: User {user_id} not changed")
        return Response({"message":"User wasn't update"},status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@jwt_user_id_compare
def log_out(request,user_id, clear = True):
    print(f"[{datetime.datetime.now()}]info: User {user_id} log out")
    return Response({"message":"You log out successfully"},status=status.HTTP_200_OK)

@api_view(['POST'])
@jwt_user_id_compare
def upload_file(request,user_id):
    if 'file' not in request.FILES:
        print(f"[{datetime.datetime.now()}]error: User {user_id} not sent file")
        return Response({"message":" File not sent"},status=status.HTTP_403_FORBIDDEN)
    else:           
        file = request.FILES['file']
        description = request.data['description'] if request.data['description'] else None
        new_file = FileView()
        if new_file.add_file(user_id=user_id,file=file,description=description):
            print(f"[{datetime.datetime.now()}]info: File {file.name} uploaded")
            return Response({"message":"File upload successfully"},status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: Failed upload file by user {user_id}")
    return Response({"message":"File upload failed"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@jwt_user_id_compare
def get_all_files(request,user_id):
    file_view = FileView()
    all_files = file_view.get_all_user_files(user_id=user_id)
    if all_files:
        serializer = FileSerializer(all_files, many=True)
        print(f"[{datetime.datetime.now()}]info: Files {user_id} sended to")
        return Response({"files": serializer.data},status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: User {user_id} don't get all files")
    return Response({"message":"Failed to retrieve files try again"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@jwt_user_id_compare
def get_file_by_id(request,user_id,file_id):
    file_view = FileView()
    file = file_view.get_file(file_id=file_id)
    
    file_path = os.path.join(f'../cloud_store/{file.user.id}', file.name)

    if file:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as result:
                response = HttpResponse(result.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{file.name}"'
                print(f"[{datetime.datetime.now()}]info: File {file.name} sended")
                return response
    
    print(f"[{datetime.datetime.now()}]error: User {user_id} not get file {file_id}")
    return Response({"message":"Failed to retrive your file try again"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_file_by_link(request,link):
    file_view = FileView()
    file = file_view.get_file(link=link)

    file_path = os.path.join(f'../cloud_store/{file.user.id}', file.name)

    if file:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as result:
                response = HttpResponse(result.read(), content_type=mimetypes.guess_type(file_path)[0])
                ru = 'ru'
                response['Content-Disposition'] = f'attachment; filename="{translit(file.name,ru,reversed=True)}"'
                print(f"[{datetime.datetime.now()}]info: File {file.name} sended by link")
                return response
        
    print(f"[{datetime.datetime.now()}]error: File {file.id} didn't get by link")
    return Response({"message":"Failed to retrive your file try again"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@jwt_user_id_compare
def get_file_link(request,user_id,file_id):
    file_view = FileView()
    link = file_view.get_file_link(file_id=file_id)
    if link:
        print(f"[{datetime.datetime.now()}]info: User {user_id} create link for file {file_id}")
        return Response({"link": link},status=status.HTTP_200_OK)
    
    print(f"[{datetime.datetime.now()}]error: Failed creating link for file {file_id} by user {user_id}")
    return Response({"message":"Failed to get file link try again"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@jwt_user_id_compare
def delete_file(request,user_id,file_id):
    file_view = FileView()
    if file_view.delete_file(file_id=file_id):
        print(f"[{datetime.datetime.now()}]info: User {user_id} delete file {file_id}")
        return Response({"message":"File deleted successfully"},status=status.HTTP_200_OK)

    print(f"[{datetime.datetime.now()}]error: Failed delete file {file_id} by user {user_id}")
    return Response({"message":"File wasn't delete"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@jwt_user_id_compare
def update_file(request,user_id,file_id):
    file_view = FileView()
    data = request.data
    file = file_view.change_file(file_id=file_id, data=data)
    if file:
        print(f"[{datetime.datetime.now()}]info: User {user_id} change description file {file_id}")
        return Response({"message":"File updated successfully"}, status=status.HTTP_200_OK)           
    
    print(f"[{datetime.datetime.now()}]error: File {file_id} not updated by user {user_id}")
    return Response({"message":"File not updated"},status=status.HTTP_403_FORBIDDEN)  



    