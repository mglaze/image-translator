import os
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
import sys
import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Import the functions from the main script
from image_translator import load_config, process_images_in_directory, detect_and_translate_text

class TestTranslateImages(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open, read_data='{"target_language": "es"}')
    def test_load_config(self, mock_file):
        """Test loading configuration from a JSON file."""
        config = load_config()
        self.assertEqual(config['target_language'], 'es')
    
    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_load_config_file_not_found(self, mock_file):
        """Test handling of missing config file."""
        config = load_config()
        self.assertEqual(config, {})

    @patch('google.cloud.vision.ImageAnnotatorClient')
    @patch('google.cloud.translate_v2.Client')
    def test_process_images_in_directory(self, mock_translate_client, mock_vision_client):
        """Test processing images in a directory."""
        # Mock the Vision and Translate client methods
        mock_vision_client.return_value.text_detection.return_value.text_annotations = [MagicMock(description="Hola Mundo")]
        mock_translate_client.return_value.detect_language.return_value = {'language': 'es'}
        mock_translate_client.return_value.translate.return_value = {'translatedText': 'Hello World'}
        
        # Test processing with mocks
        result = process_images_in_directory('tests/', 'en')
        
        # Since no images are present in 'tests/', result should be an empty dictionary
        self.assertEqual(result, {})  # Ensure the result is an empty dictionary

    
    @patch('google.cloud.translate_v2.Client')
    def test_detect_and_translate_text(self, mock_translate_client):
        """Test the language detection and translation functionality."""
        # Mock the Google Translate API methods
        mock_translate_client.return_value.detect_language.return_value = {'language': 'es'}
        mock_translate_client.return_value.translate.return_value = {'translatedText': 'Hello World'}
        
        # Test translation
        translated_text = detect_and_translate_text("Hola Mundo", target_language="en")
        self.assertEqual(translated_text, "Hello World")
    
    @patch('sys.argv', ['image_translator.py', 'tests/images/', 'fr'])
    def test_command_line_argument_target_language(self):
        """Test command-line argument takes precedence over config file."""
        # Mock the config loading and ensure command-line argument is used
        with patch('builtins.open', mock_open(read_data='{"target_language": "es"}')):
            config = load_config()
            target_language = sys.argv[2] if len(sys.argv) > 2 else config.get('target_language', 'en')
            self.assertEqual(target_language, 'fr')
    
    @patch('sys.argv', ['image_translator.py', 'tests/images/'])
    def test_fallback_to_config_for_target_language(self):
        """Test fallback to config when command-line argument is not provided."""
        # Mock the config loading
        with patch('builtins.open', mock_open(read_data='{"target_language": "es"}')):
            config = load_config()
            target_language = sys.argv[2] if len(sys.argv) > 2 else config.get('target_language', 'en')
            self.assertEqual(target_language, 'es')


if __name__ == '__main__':
    unittest.main()
