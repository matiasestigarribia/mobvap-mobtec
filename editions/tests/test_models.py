import shutil
import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from editions.models import Edition

MEDIA_ROOT_TEST = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class EditionModelTest(TestCase):
    
    @classmethod
    def tearDowndClass(cls):
        shutil.rmtree(MEDIA_ROOT_TEST, ignore_errors=True)
        super().tearDownClass()
        
    def setUp(self):
        self.image_content = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x05\x04\x04'
            b'\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44'
            b'\x01\x00\x3b'
        )
        self.uploaded_image = SimpleUploadedFile(
            name='test_image.gif',
            content=self.image_content,
            content_type='image/gif'
        ) 
    
    def test_slug_automation(self):
        edition = Edition.objects.create(
            edition_name='eDiCao tESte 2026',
            edition_description='asds',
            preview_image1=self.uploaded_image,
            preview_image2=self.uploaded_image
        )
        self.assertEqual(edition.slug, "edicao-teste-2026")
    
    def test_image_processing(self):
        edition = Edition.objects.create(
            edition_name="Foto Teste",
            edition_description='desc',
            preview_image1=self.uploaded_image,
            preview_image2=self.uploaded_image
        )
        
        self.assertTrue(edition.preview_image1.name)
        self.assertTrue(edition.preview_image1.size > 0)
        self.assertTrue(edition.preview_image2.name)
        self.assertTrue(edition.preview_image2.size > 0)
    
    def test_unique_slug_constraint(self):
        Edition.objects.create(
            edition_name='Mesmo Nome',
            edition_description='desc 1',
            preview_image1=self.uploaded_image,
            preview_image2=self.uploaded_image
        )

        with self.assertRaises(Exception):
            Edition.objects.create(
                edition_name='Mesmo Nome',
                edition_description="desc 2",
                preview_image1=self.uploaded_image,
                preview_image2=self.uploaded_image
            )