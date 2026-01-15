import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock firebase_admin before importing SarahChat
sys.modules["firebase_admin"] = MagicMock()
sys.modules["firebase_admin.db"] = MagicMock()

from Sarah_Chat import SarahChat
from Gemini_Genesis_Core import GeminiGenesisCore

class TestGenesisIntegration(unittest.TestCase):
    def setUp(self):
        # Mock environment variable
        os.environ["GEMINI_API_KEY"] = "fake_key"
        
        # Mock DB
        self.mock_db = MagicMock()
        
    def tearDown(self):
        if "GEMINI_API_KEY" in os.environ:
            del os.environ["GEMINI_API_KEY"]

    @patch("Sarah_Chat.GeminiGenesisCore")
    def test_chat_uses_genesis_core(self, MockGenesisCore):
        # Setup Mock
        mock_core_instance = MockGenesisCore.return_value
        mock_core_instance.client = MagicMock() # For backwards compat
        mock_core_instance.generate_content_safe.return_value = "Genesis Response"
        
        # Initialize Chat
        chat = SarahChat(self.mock_db)
        
        # Verify Initialization
        MockGenesisCore.assert_called_with("fake_key")
        self.assertEqual(chat.genesis_core, mock_core_instance)
        
        # Test Generate Response
        response = chat.generate_response("Hello Sarah")
        
        # Verify Response
        self.assertEqual(response, "Genesis Response")
        
        # Verify generate_content_safe was called
        mock_core_instance.generate_content_safe.assert_called_once()
        
        # Verify arguments passed to generate_content_safe
        call_args = mock_core_instance.generate_content_safe.call_args
        self.assertEqual(call_args.kwargs["user_input"], "Hello Sarah")
        self.assertIn("history", call_args.kwargs)

    @patch("Sarah_Chat.GeminiGenesisCore")
    def test_saul_injection(self, MockGenesisCore):
        # Setup Mock
        mock_core_instance = MockGenesisCore.return_value
        mock_core_instance.client = MagicMock()
        mock_core_instance.generate_content_safe.return_value = "Genesis Response"
        
        # Initialize Chat
        chat = SarahChat(self.mock_db)
        
        # Inject SAUL
        mock_saul = MagicMock()
        chat.saul = mock_saul
        
        # Test Generate Response
        chat.generate_response("Test with SAUL")
        
        # Verify SAUL was passed to core
        self.assertEqual(mock_core_instance.saul, mock_saul)

if __name__ == "__main__":
    unittest.main()
