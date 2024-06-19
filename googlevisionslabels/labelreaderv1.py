import io
import os
from google.cloud import vision

# Set your Google Cloud credentials environment variable
# export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"

def detect_text(image_file):
    """Detects text in an image file using Google Vision API."""
    client = vision.ImageAnnotatorClient()

    with io.open(image_file, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    else:
        return "No text found in the image."

if __name__ == '__main__':
    # Path to the image file
    image_file_path = 'label.jpg'

    # Check if the file exists
    if not os.path.exists(image_file_path):
        print("File not found.")
    else:
        # Perform OCR
        extracted_text = detect_text(image_file_path)

        # Output the extracted text
        print("Extracted Text:")
        print(extracted_text)
