import shutil
import tempfile
from unittest.mock import patch, MagicMock
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import ProtectedError
from editions.models import Edition
from videos.models import Video


MEDIA_ROOT_TEST =tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT_TEST)
class VideoModelTest(TestCase):
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT_TEST, ignore_errors=True)
        super().tearDownClass()
    
    def setUp(self):
        self.edition = Edition.objects.create(
            edition_name="Video edition test",
            edition_description='desc'
        )
        self.video_content = b'fake_video_content'
        self.uploaded_video = SimpleUploadedFile(
            name='my_video.mp4',
            content=self.video_content,
            content_type='video/mp4'
        )
        
    @patch('videos.models.process_video')
    def test_save_calls_process_video(self, mock_process_video):
        processed_file_mock = SimpleUploadedFile('processed.mp4', b'video_ok', 'video/mp4')
        thumbnail_mock = SimpleUploadedFile('thumb.jpg', b'img', 'image/jpeg')
        mock_process_video.return_value = (processed_file_mock, thumbnail_mock)
        
        video = Video.objects.create(
            video_title="Mocked Video",
            video_file=self.uploaded_video,
            edition=self.edition
        )
        
        mock_process_video.assert_called_once()
        
        self.assertTrue(video.video_thumbnail)
        self.assertIn('thumb.jpg', video.video_thumbnail.name)
    
    @patch('videos.models.process_video')
    def test_protect_edition_deletion(self, mock_process_video):
        mock_process_video.return_value = (self.uploaded_video, SimpleUploadedFile('t.jpg', b''))
    
        Video.objects.create(
            video_title="Protected video",
            video_file=self.uploaded_video,
            edition=self.edition
        )
        
        with self.assertRaises(ProtectedError):
            self.edition.delete()