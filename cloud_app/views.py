from .models import File, User
import datetime, os, shutil

class FileView:
    def get_all_files(self):
        try:
            files = File.objects.all()
            print(f"[{datetime.datetime.now()}]info: Get all files")
            return files
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: Don't get all files because {str(e)}")
            return None
        
        
    def get_all_user_files(self, user_id):
        try:
            user = User.objects.get(id=user_id)
            files = File.objects.filter(user=user)
            print(f"[{datetime.datetime.now()}]debug: User {user_id} get all files")
            return files
        
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: User {user_id} don't get all files because {str(e)}")
            return None
        
    def get_file(self, link = None, file_id = None):
        try:
            if file_id is not None:
                file = File.objects.get(id=file_id)
                file.last_download = datetime.datetime.now()
                file.save()
                print(f"[{datetime.datetime.now()}]debug: File {file.name} geted by id")
            
            elif link:
                file = File.objects.get(link=link)
                file.last_download = datetime.datetime.now()
                file.save()
                print(f"[{datetime.datetime.now()}]debug: File {file.name} geted by link")
            else:
                print(f"[{datetime.datetime.now()}]error: File not found ")
                return None
            return file
        
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: File don't geted because {str(e)}")
            return None

    
    def add_file(self, user_id, file, description):
        try:
            user = User.objects.get(id=user_id)
            size = file.size
            filename = file.name

            # Проверяем существует ли файл с таким именем в папке пользователя
            user_folder = os.path.join('../cloud_store', str(user_id))
            destination_path = os.path.join(user_folder, filename)
            if os.path.exists(destination_path):
                # Файл с таким именем уже существует, переименовываем его
                filestem, fileext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(destination_path):
                    new_filename = f"{filestem} ({counter}){fileext}"
                    destination_path = os.path.join(user_folder, new_filename)
                    counter += 1
                filename = new_filename

            # Создаем запись о файле в базе данных
            new_file = File.objects.create(
                name=filename,
                size=size,
                user=user,
                description=description,
            )

            # Сохраняем файл на диск
            with open(destination_path, 'wb') as destination_file:
                for chunk in file.chunks():
                    destination_file.write(chunk)            

            print(f"[{datetime.datetime.now()}]debug: User {user.username} added file {filename}")
            return True

        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: Failed to add file by user {user_id}: {str(e)}")
            return False

        
    def delete_file(self, file_id):
        try:
            file = File.objects.get(id=file_id)
            os.remove(f'../cloud_store/{file.user.id}/{file.name}')
            file.delete()
            print(f"[{datetime.datetime.now()}]debug: User {file.user.username} delted file {file.name}")
            return True
        
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: Don't delte file because {str(e)}")
            return False

    def change_file(self,file_id,data):
        try:
            file = File.objects.get(id=file_id)
            if "filename" in data:
                new_filename = data["filename"]
                file_path = f"../cloud_store/{file.user.id}/{file.name}"
                parent_dir = os.path.dirname(file_path)
                new_file_path = os.path.join(parent_dir, new_filename)
                os.rename(file_path, new_file_path)
                
                file.name = new_filename

            if 'description' in data:
                file.description = data['description']
            
            file.save()
            print(f"[{datetime.datetime.now()}]debug: User {file.user.username} change file name for file {file.id}")
            return file
        
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: Don't change filename because {str(e)}")
            return None


    def get_file_link(self,file_id):
        try:
            file = File.objects.get(id=file_id)
            print(f"[{datetime.datetime.now()}]debug: Generated link for file {file.id}")
            return file.generate_link()
        
        except Exception as e:
            print(f"[{datetime.datetime.now()}]error: Don't get file link because {str(e)}")
            return None
