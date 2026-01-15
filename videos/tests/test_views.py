from unittest.mock import patch
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework import status
from editions.models import Edition
from videos.models import Video


@override_settings(SECURE_SSL_REDIRECT=False)
class VideoViewTest(TestCase):
    
    @patch('videos.models.process_video')
    def setUp(self, mock_process):
        mock_process.return_value = (
            SimpleUploadedFile('p.mp4', b''),
            SimpleUploadedFile('t.jpg', b'')
        )
        
        self.client = APIClient()
        self.edition = Edition.objects.create(
            edition_name='Video Edition view',
            edition_description='desc'
        )
        
        self.video = Video.objects.create(
            video_title='Video View test',
            video_file=SimpleUploadedFile('v.mp4', b'content'),
            edition=self.edition
        )
        
        self.list_url = f'/api/v1/editions/{self.edition.slug}/videos/'
    
    def test_list_video_success(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(data), 1)
        
    def test_create_video_forbidden(self):
        data={'video_title': 'Hacker video'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
