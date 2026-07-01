# ocr.py
import easyocr
import os

# Khởi tạo reader một lần duy nhất (singleton pattern) để tái sử dụng
_reader = None

def get_reader(lang=['en']):
    global _reader
    if _reader is None:
        print("Đang khởi tạo EasyOCR Reader...")
        _reader = easyocr.Reader(lang)
    return _reader

def extract_text_from_image(image_path="test.png", lang=['en']):
    print("Đang trích xuất văn bản bằng EasyOCR...")
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy file {image_path}")
        return ""
    
    reader = get_reader(lang)
    result = reader.readtext(image_path)
    
    extracted_text = " ".join([res[1] for res in result])
    print("\n--- KẾT QUẢ OCR ---")
    print(extracted_text if extracted_text else "(Không tìm thấy văn bản)")
    print("-------------------\n")
    return extracted_text
