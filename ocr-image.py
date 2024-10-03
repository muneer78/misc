import easyocr
import pyperclip
import cv2
import certifi
import ssl

# Set up the SSL context using certifi's certificate bundle
ssl_context = ssl.create_default_context(cafile=certifi.where())


def preprocess_image(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)

    # Convert the image to grayscale for better OCR accuracy
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Optional: Apply a threshold to clean up the image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    return thresh

def image_to_text(image_path):
    # Preprocess the image using OpenCV
    processed_image = preprocess_image(image_path)
    
    # Initialize the EasyOCR reader
    reader = easyocr.Reader(['en'])  # 'en' for English language
    
    # Perform OCR on the processed image
    result = reader.readtext(processed_image, detail=0)  # Extract text without bounding boxes
    
    # Join the list of text into a single string
    text = "\n".join(result)
    
    return text

def copy_to_clipboard(text):
    pyperclip.copy(text)
    print("Text copied to clipboard.")

# Example usage
image_path = r'/Users/muneer78/Downloads/img_9NmawCF.jpg'  # Replace with your image file path
text = image_to_text(image_path)
copy_to_clipboard(text)

# You can also print the text to confirm
print("Extracted Text:\n", text)
