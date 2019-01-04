from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage


class FileManager(models.Manager):
    def create_file(self, title, upload_by, file_link):
        file = self.create(
            title=title,
           upload_by=upload_by,
           file_link=file_link
       )
        return file


class File(models.Model):
    title = models.CharField(max_length=200, null=True)
    upload_by = models.IntegerField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    file_link = models.CharField(max_length=300, null=True)
    # media_file = models.FileField()

    objects = FileManager()



