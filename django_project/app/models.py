import hashlib

from django.core.files.storage import FileSystemStorage
from django.db import models


class UploadFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if max_length and len(name) > max_length:
            raise (Exception("name's length is greater than max_length"))
        return name

    def _save(self, name, content):
        name_md5 = md5_for_file(content.chunks())
        try:
            exist_file = File.objects.filter(md5sum=name_md5).earliest("date")
            return str(exist_file.file)
        except File.DoesNotExist:
            return super(UploadFileSystemStorage, self)._save(name, content)


def md5_for_file(chunks):
    md5 = hashlib.md5()
    for data in chunks:
        md5.update(data)
    return md5.hexdigest()


class File(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    upload_by = models.IntegerField(blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    public_link = models.CharField(max_length=300, null=True)
    file = models.FileField(
        upload_to="uploads/%Y/",
        default=None,
        storage=UploadFileSystemStorage()
    )
    is_deleted = models.BooleanField(blank=True, default=False)
    md5sum = models.CharField(max_length=36, blank=True)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:
            md5 = hashlib.md5()
            for chunk in self.file.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super(File, self).save(*args, **kwargs)
