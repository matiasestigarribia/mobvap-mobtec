from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from editions.models import Edition

@override_settings(SECURE_SSL_REDIRECT=False)
class EditionViewTest(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.edition = Edition.objects.create(
            edition_name="Test Edition",
            edition_description='Desc'
        )
        
    def test_list_editions_success(self):
        response = self.client.get('/api/v1/editions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_edition_method_not_allowed(self):
        data = {'edition_name': 'Hacker Edition'}
        response = self.client.post('/api/v1/editions/', data)
        
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_delete_edition_method_not_allowed(self):
        
        response = self.client.delete(f'/api/v1/editions/{self.edition.edition_name}/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
