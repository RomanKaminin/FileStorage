from django.db import models
from django.core.files.storage import FileSystemStorage


class UploadFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise(Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        if self.exists(name):
            return name
        return super(UploadFileSystemStorage, self)._save(name, content)


class File(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    upload_by = models.IntegerField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    public_link = models.CharField(max_length=300, null=True)
    file = models.FileField(upload_to='uploads/%Y/',default=None, storage=UploadFileSystemStorage())
    is_deleted = models.BooleanField(blank=True, default=False)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

