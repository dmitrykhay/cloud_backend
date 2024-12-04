from rest_framework import serializers
from .models import File, User

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    total_size = serializers.SerializerMethodField()
    file_count = serializers.SerializerMethodField()

    def get_total_size(self, obj):
        files = File.objects.filter(user=obj)
        total_size = 0
        for file in files:
            total_size += file.size
        return total_size

    def get_file_count(self, obj):
        return File.objects.filter(user=obj).count()
    
    
    class Meta:
        model = User
        fields = ['id','username','email','is_staff','total_size', 'file_count' ]