from django.test import TestCase
from unittest.mock import patch
from comments.models import Comment


class CommentSignalTests(TestCase):
    
    def setUp(self):
        self.comment_text = "Chaos test text"
        self.author = "Tester Chaos"
        
    
    @patch('comments.signals.moderate_comment')
    def test_signal_resilience_on_failure(self, mock_moderate):
        mock_moderate.side_effect = Exception("Critical Error: Azure offline")
        
        try:
            comment = Comment.objects.create(
                comment_author=self.author,
                comment_text=self.comment_text
            )
        except Exception as e:
            self.fail(f"Failed Test! Azure error broke create comment")
        
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())
        
        comment.refresh_from_db()
        self.assertEqual(comment.comment_status, 'pending')