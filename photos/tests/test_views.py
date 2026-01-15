from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from editions.models import Edition
from photos.models import Photo


@override_settings(SECURE_SSL_REDIRECT=False)
class PhotoViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.edition = Edition.objects.create(
            edition_name="Edition View",
            edition_description="Desc"
        )
        self.photo = Photo.objects.create(
            image_title="Photo 1",
            edition=self.edition,
            image_file='path/false/photo.jpg'
        )
        
        self.list_url = f'/api/v1/editions/{self.edition.slug}/photos/'
    
    def test_list_photos_success(self):
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)
    
    def test_create_photo_forbidden(self):
        data = {'image_title': 'Hacker Photo'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
