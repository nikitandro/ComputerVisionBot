import cv2
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:/Users/cherr/AppData/Local/Tesseract-OCR/tesseract.exe'


def image_to_text(input_file, lang, preprocess="thresh"):

    image = cv2.imread(input_file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)

    cv2.imwrite(input_file, gray)

    text = pytesseract.image_to_string(Image.open(input_file), lang=lang)
    return text
