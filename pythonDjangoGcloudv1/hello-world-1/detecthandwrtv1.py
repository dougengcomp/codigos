from google.cloud import vision
import io

def detect_handwritten_text(image_path):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Performs handwritten text detection
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    # Extracts handwritten text
    handwritten_text = ''
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    handwritten_text += word_text + ' '

    return handwritten_text

# Example usage
if __name__ == "__main__":
    # Provide the path to your handwritten JPEG image file
    image_path = r"C:\Users\rijul\Downloads\test4.jpg"
    
    # Perform handwritten text recognition using Google Cloud Vision API
    recognized_text = detect_handwritten_text(image_path)
    
    # Print the recognized text
    print("Recognized Handwritten Text:")
    print(recognized_text)
