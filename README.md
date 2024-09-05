# Image Translator with Google Cloud Vision and Translate

A Python script that uses Google Cloud Vision to extract text from images and automatically detects and translates the text into the desired language using Google Cloud Translation API. It can handle multiple images in a directory.

## Features

- Extract text from images using Google Cloud Vision API
- Automatically detect the language of the text
- Translate the text to a target language using Google Cloud Translate API
- Process multiple images in a specified directory
- Supports common image formats (JPG, PNG, etc.)

## Requirements

- Python 3.6+
- Google Cloud Service Account credentials
- Enabled Google Cloud Vision and Translate APIs

### Dependencies

You can install the required dependencies via pip using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Setup

#### 1. Google Cloud Setup

1. Create a Google Cloud project: [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Google Cloud Vision API** and **Google Cloud Translation API**.
3. Create a Service Account with appropriate permissions and download the JSON credentials file.
4. Set the environment variable to point to your credentials file:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path_to_your_service_account.json"
   ```

#### 2. Clone the repository
   ```bash
   git clone https://github.com/yourusername/translate_images.git
   cd image-translator
   ```
#### 3. Install Dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Usage
   ```bash
   python image_translator.py <directory_path> [target_language]
   ```
   - <directory_path>: The directory containing images (JPG/PNG).
   - [target_language]: (Optional) The language code to translate to (default is English: en).

## Run Tests
  ```bash
   pytest -v
  ```
  
### Example

To translate all images in the /home/user/images folder to English:

  ```bash
  python image_translator.py /home/user/images en
  ```
## Example Image Processing Output

  ```bash
    Processing image1.jpg...
    Detected language: es
    Extracted Text from image1.jpg:
    Hola Mundo!

    Translated Text from image1.jpg:
    Hello World!

    Processing examples/image-jp2.png...
    Extracted Text from examples/image-jp2.png:
    自分で売った
    喧嘩やろ
    自分で
    片つけんのが
    筋ちゃうんか!
    it
    yourself!!!!
    Detected language: ja
    Translated Text from examples/image-jp2.png:
    You started this fight, shouldn&#39;t you settle it yourself?!

  ```

## Contributing

Contributions are welcome! Please fork the repository and create a pull request. For major changes, please open an issue first to discuss what you'd like to change.

### Steps to Contribute
 1. Fork the repository.
 2. Create your feature branch (`git checkout -b feature/new-feature`).
 3. Commit your changes (`git commit -m 'Add some feature'`).
 4. Push to the branch (`git push origin feature/new-feature`).
 5. Open a pull request.

## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
