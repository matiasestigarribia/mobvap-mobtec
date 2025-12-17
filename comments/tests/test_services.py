from django.test import TestCase
from unittest.mock import patch, MagicMock
from comments.services import moderate_comment


class ContentSafetyLogicTests(TestCase):
    
    def setUp(self):
        self.text = "sample text"
    
    @patch('comments.services.get_azure_analysis')
    def test_logic_rejects_high_severity(self, mock_get_analysis):
        mock_response = MagicMock()
        mock_category = MagicMock()
        mock_category.severity = 5
        
        mock_response.categories_analysis = [mock_category]
        mock_get_analysis.return_value = mock_response
        
        status, _ = moderate_comment(self.text)
        self.assertEqual(status, 'not_approved')
        
    @patch('comments.services.get_azure_analysis')
    def test_logic_approves_low_severity(self, mock_get_analysis):
        mock_response = MagicMock()
        mock_category = MagicMock()
        mock_category.severity = 0
        
        mock_response.categories_analysis = [mock_category]
        mock_get_analysis.return_value = mock_response
        
        status, _ = moderate_comment(self.text)
        
        self.assertEqual(status, 'approved')
        
    @patch('comments.services.get_azure_analysis')
    def test_logic_pending_mid_severity(self, mock_get_analysis):
        mock_response = MagicMock()
        mock_category = MagicMock()
        mock_category.severity = 2
        
        mock_response.categories_analysis = [mock_category]
        mock_get_analysis.return_value = mock_response
        
        status, _ = moderate_comment(self.text)
        
        self.assertEqual(status, 'pending')
