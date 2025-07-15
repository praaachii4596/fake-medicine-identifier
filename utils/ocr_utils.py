import easyocr
import cv2
import numpy as np
import re
from datetime import datetime

# Initialize EasyOCR reader (English only, CPU mode)
reader = easyocr.Reader(['en'], gpu=False)

def preprocess_image(path):
    """
    Load and preprocess the image to improve OCR accuracy:
    - Resize for clarity
    - Convert to grayscale
    - Apply adaptive thresholding
    - Deskew the image if tilted
    Returns the processed image.
    """
    image = cv2.imread(path)

    # Resize image (2x zoom) for better readability
    image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to enhance contrast
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    # Deskew the image (correct tilt)
    deskewed = deskew(thresh)
    return deskewed

def deskew(image):
    """
    Correct skew/tilt in the given binary image.
    Returns the rotated image aligned horizontally.
    """
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Compute rotation matrix and rotate image
    (h, w) = image.shape
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return rotated

def extract_text_from_image(image_path):
    """
    Run OCR on the given image using EasyOCR after preprocessing.
    Returns the detected text as a single string.
    """
    processed_image = preprocess_image(image_path)
    results = reader.readtext(processed_image)

    # Concatenate detected text lines
    text_output = " ".join([text for _, text, _ in results])
    return text_output

def extract_expiry_date(text):
    """
    Extract expiry date from text using regular expressions.
    Supports:
    - MM/YYYY
    - DD-MM-YYYY (and similar formats with / or .)
    
    Returns a datetime object if found, otherwise None.
    """
    patterns = [
        r"(0[1-9]|1[0-2])[/\-\.](\d{4})",        # MM/YYYY
        r"(\d{2})[/\-\.](\d{2})[/\-\.](\d{4})",  # DD-MM-YYYY
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                if len(match) == 2:
                    # Format: MM/YYYY
                    month, year = match
                    return datetime(int(year), int(month), 1)
                elif len(match) == 3:
                    # Format: DD-MM-YYYY
                    day, month, year = match
                    return datetime(int(year), int(month), int(day))
            except ValueError:
                continue

    return None  # No valid date found