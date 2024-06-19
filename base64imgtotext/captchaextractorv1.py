from google.cloud import vision
import io
import base64

def detect_text(base64_image):
    # Initialize the Google Cloud Vision client
    client = vision.ImageAnnotatorClient()

    # Decode the base64-encoded image
    image = vision.Image(content=base64.b64decode(base64_image))

    # Perform text detection on the image
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        return texts[0].description
    else:
        return "No text found in the image."

def main():
    # Load the JPG file
    with open("capturavaldir.png", "rb") as image_file:
        # Convert the image to base64
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Run Google Vision to extract text from the image
    extracted_text = detect_text(base64_image)
    print("Text extracted from the image:")
    print(extracted_text)

if __name__ == "__main__":
    main()
