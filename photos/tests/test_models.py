import shutil
import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import ProtectedError
from editions.models import Edition
from photos.models import Photo

MEDIA_ROOT_TEST = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class PhotoModelTest(TestCase):
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT_TEST, ignore_errors=True)
        super().tearDownClass()
        
    def setUp(self):
        self.edition = Edition.objects.create(
            edition_name='test photo edition',
            edition_description="Desc"
        )
    
        self.image_content = (
                b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04'
                b'\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44'
                b'\x01\x00\x3b'
            )
        self.uploaded_image = SimpleUploadedFile(
            name='photo.jpg',
            content=self.image_content,
            content_type='image/jpeg'
        )
    
    def test_create_photo_success(self):
        photo = Photo.objects.create(
            image_title="My Picture",
            image_file=self.uploaded_image,
            edition=self.edition
        )
    
        self.assertTrue(photo.image_file.name)
        self.assertEqual(photo.edition, self.edition)
        self.assertEqual(str(photo), "My Picture")
        
    def test_protect_edition_deletion(self):
        Photo.objects.create(
            image_title="Protected Photo",
            image_file=self.uploaded_image,
            edition=self.edition
        )
        
        with self.assertRaises(ProtectedError):
            self.edition.delete()