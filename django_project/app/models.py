from django.db import models
from django.contrib.auth.models import User


class File(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    upload_by = models.IntegerField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    file_link = models.CharField(max_length=300, null=True)
    file = models.FileField(upload_to='uploads/%Y/',default=None)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

