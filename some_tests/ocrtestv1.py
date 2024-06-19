import pytesseract
from PIL import Image

def ocr_png(image_path):
    # Open the PNG image using PIL (Python Imaging Library)
    with Image.open(image_path) as img:
        # Convert the PNG image to RGB mode if it's not already in that mode
        if img.mode != "RGB":
            print("Image mode is:", img.mode)
            img = img.convert("RGB")
            print("Image converted to RGB")
        
        # Perform OCR using pytesseract
        text = pytesseract.image_to_string(img)
        return text

# Example usage
if __name__ == "__main__":
    # Provide the path to your PNG image file
    image_path = r"C:\Users\rijul\Downloads\test2.jpg"
    
    # Perform OCR on the image
    text_content = ocr_png(image_path)
    
    # Print the extracted text content
    print("OCR Result:")
    print(text_content)
