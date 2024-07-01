import cv2
import pytesseract
from pytesseract import Output
import re
import unstructured_pytesseract
import numpy as np
from scipy.ndimage import interpolation as inter
import tkinter as tks

unstructured_pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

# # Funkcja do wyciągania produktów i cen z tekstu
# def extract_products_and_prices(text):
#     products_and_prices = []
#     lines = text.split('\n')
#     for line in lines:
#         match = re.match(r'(.*?)(\d+,\d{2})\s?zł', line)
#         if match:
#             product = match.group(1).strip()
#             price = match.group(2).replace(',', '.').strip()
#             products_and_prices.append((product, float(price)))
#     return products_and_prices


def correct_skew(image, delta=1, limit=5):
    def determine_score(arr, angle):
        data = inter.rotate(arr, angle, reshape=False, order=0)
        histogram = np.sum(data, axis=1, dtype=float)
        score = np.sum((histogram[1:] - histogram[:-1]) ** 2, dtype=float)
        return histogram, score

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] 

    scores = []
    angles = np.arange(-limit, limit + delta, delta)
    for angle in angles:
        histogram, score = determine_score(thresh, angle)
        scores.append(score)

    best_angle = angles[scores.index(max(scores))]

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, best_angle, 1.0)
    corrected = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, \
            borderMode=cv2.BORDER_REPLICATE)
    
    return best_angle, corrected

def remove_noise(image):
    return cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 15)

# Funkcja do przetwarzania obrazu i wyciągania tekstu
def process_receipt_image(image_path, show=False):
    # Wczytaj obraz
    image = cv2.imread(image_path)
    _, image = correct_skew(image)
    image = remove_noise(image)

    # Przekształć obraz na skalę szarości
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Zastosuj progowanie, aby zwiększyć kontrast
    _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh_image = cv2.morphologyEx(thresh_image, cv2.MORPH_OPEN, (5,5), iterations=5)

    if show:
        cv2.imshow('image',thresh_image)
        cv2.waitKey(0)

    # Użyj pytesseract do wyciągania tekstu z obrazu
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(thresh_image, config=custom_config, lang='pol')
    
    # # Wyciągnij produkty i ceny
    # products_and_prices = extract_products_and_prices(text)
    # return products_and_prices
    return text

if __name__ == "__main__":
    # Ścieżka do obrazu paragonu
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename()
    # Przetwarzaj obraz i wyciągnij dane
    text = process_receipt_image(image_path)

    print(text)