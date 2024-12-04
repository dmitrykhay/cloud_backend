import os, datetime
from .models import User
from django.contrib.auth.hashers import make_password


class UserView:
    def get_user(self,username):
        try:
            user = User.objects.get(username=username)
            user.last_login = datetime.datetime.now()
            user.save()
            print(f"[{datetime.datetime.now()}]debug: Get {user.username} user")
            return user
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: {str(e)}")
            return None
    
    def get_all_users(self):
        users = User.objects.all()
        print(f"[{datetime.datetime.now()}]debug: Get all user")
        return users

    def create_user(self, data):
        try:
            new_user = User.objects.create(
                username = data['username'],
                password = data['password'],
                email = data['email'],
            )
            new_user.folder = new_user.id
            new_user.save()
            os.chdir("../cloud_store")
            os.mkdir(f'{new_user.id}')
            new_user.folder = new_user.id
            print(f"[{datetime.datetime.now()}]debug: Create new user {new_user.id}")
            return new_user
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: {str(e)}")
            return None
    
    def delete_user(self, user_id):
        try:
            delete_user = User.objects.get(id=user_id)
            delete_user.delete()
            user_folder = os.path.join("../cloud_store", str(user_id))
            for file_name in os.listdir(user_folder):
                file_path = os.path.join(user_folder, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)  
            os.rmdir(user_folder)
            print(f"[{datetime.datetime.now()}]debug: User {user_id} deleted successfully")
            return True 
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: {str(e)}")
            return False

    def update_user(self,user_id, data):
        try:
            update_user = User.objects.get(id=user_id)
            update_user.folder = update_user.id
            if 'username' in data:
                update_user.username = data['username']
            if 'email' in data:
                update_user.email = data['email']
            if 'password' in data and data['password']:
                update_user.password = make_password(data['password'])
                
            update_user.save()
            print(f"[{datetime.datetime.now()}]debug: User {user_id} updated successfully")
            return update_user
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: {str(e)}")
            return None 

    def change_premissions(self,user_id):
        try:
            user = User.objects.get(id=user_id)
            user.is_staff = not user.is_staff
            user.save()
            print(f"[{datetime.datetime.now()}]debug: Permission {user_id} changed ")
            return user
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: {str(e)}")
            return None