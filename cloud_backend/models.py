from django.db import models
from auth_app.models import User

class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    description = models.TextField()
    date_download = models.DateField()
    last_download = models.DateField()
    link = models.CharField(max_length=200)