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

import re

def extract_text_from_image(image_path="test.png", lang=['en']):
    print("Đang trích xuất văn bản bằng EasyOCR...")
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy file {image_path}")
        return ""
    
    reader = get_reader(lang)
    
    # Sử dụng paragraph=True để EasyOCR tự động ghép các từ/chữ rời rạc thành một câu hoàn chỉnh
    # detail=0 để chỉ lấy mảng text, bỏ qua thông tin tọa độ không cần thiết
    result = reader.readtext(image_path, detail=0, paragraph=True)
    
    # Nối tất cả lại thành một đoạn văn duy nhất và lọc bỏ khoảng trắng thừa
    extracted_text = " ".join(result)
    extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
    
    print("\n--- KẾT QUẢ OCR ---")
    print(extracted_text if extracted_text else "(Không tìm thấy văn bản)")
    print("-------------------\n")
    return extracted_text
