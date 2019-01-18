import unittest
from app.models import File
from django.contrib.auth.models import User


class FileModelTest(unittest.TestCase):
    def create_file(self):
        self.user = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='r4r4r4r4'
        )
        self.file = File.objects.create(
            title="macro.txt",
            upload_by=self.user.id,
            date="2019-01-18 12:19:52.480046",
            public_link=None,
            file="uploads/2019/doc1.docx",
            is_deleted=False,
            md5sum='e7df7cd2ca07f4f1ab415d457a6e1c13',
        )
        return self.file

    def test_file_model_creation(self):
        new_file = self.create_file()
        self.assertTrue(isinstance(new_file, File))


