import os
import sys
import glob
import json
from google.cloud import vision
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv # type: ignore

# Load environment variables from .env file
load_dotenv()

# Now you can access the environment variables
credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

if credentials_path:
    print(f"Using credentials from: {credentials_path}")
else:
    print("GOOGLE_APPLICATION_CREDENTIALS not set")

# Set up the Google Cloud Vision client
vision_client = vision.ImageAnnotatorClient()

# Set up the Google Translate client
translate_client = translate.Client()

def load_config():
    """Load configuration from config/settings.json."""
    config_path = os.path.join('config', 'settings.json')
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        return {}

def extract_text_from_image(image_path):
    """Extract text from an image using Google Cloud Vision API."""
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f'{response.error.message}')

    # The first element in the response contains the full text detected
    return texts[0].description if texts else ""

def detect_and_translate_text(text, target_language="en"):
    """Detect language and translate text to the target language using Google Translate API."""
    # Detect the language of the input text
    detection = translate_client.detect_language(text)
    source_language = detection['language']

    print(f"Detected language: {source_language}")

    # Translate the text to the target language
    result = translate_client.translate(text, target_language=target_language, source_language=source_language)
    return result['translatedText']

def process_images_in_directory(directory_path, target_language="en"):
    """Process all images in a directory: extract text, detect language, and translate."""
    image_extensions = ('*.jpg', '*.jpeg', '*.png')  # Add other image formats if needed
    image_paths = []
    
    # Get all image files from the directory
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(directory_path, ext)))
    
    if not image_paths:
        print(f"No images found in directory: {directory_path}")
        return {}  # Return an empty dictionary instead of None
    
    translations = {}
    
    for image_path in image_paths:
        print(f"\nProcessing {image_path}...")
        extracted_text = extract_text_from_image(image_path)
        print(f"Extracted Text from {image_path}:\n{extracted_text}")

        translated_text = detect_and_translate_text(extracted_text, target_language=target_language)
        print(f"Translated Text from {image_path}:\n{translated_text}")

        # Store the result in a dictionary with the image filename as the key
        translations[os.path.basename(image_path)] = translated_text
    
    return translations

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <directory_path> [target_language]")
        sys.exit(1)
    
    # Directory containing images
    directory_path = sys.argv[1]

    # Load config file
    config = load_config()

    # Target language for translation, default from config if not provided
    target_language = sys.argv[2] if len(sys.argv) > 2 else config.get('target_language', 'en')

    # Process all images in the given directory
    translated_output = process_images_in_directory(directory_path, target_language)

    if translated_output:
        print("\n--- Final Translated Output ---")
        for image_name, translation in translated_output.items():
            print(f"\nImage: {image_name}\nTranslation: {translation}")
