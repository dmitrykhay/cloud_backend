from django.db import models
from auth_app.models import User
import secrets

class File(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    size = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, default=None)
    date_downloading = models.DateField(auto_now_add=True)
    last_download = models.DateField(null=True, default=None)
    link = models.CharField(max_length=200, blank=True)

    def generate_link(self):
        link = secrets.token_urlsafe(20)
        self.link = link
        self.save()
        return link

