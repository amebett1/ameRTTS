# ocr.py
import pytesseract
from PIL import Image
import os
import re

# Cấu hình đường dẫn Tesseract mặc định trên Windows (bỏ comment nếu tesseract không có trong PATH)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path="test.png", lang=['en']):
    print("Đang trích xuất văn bản bằng Tesseract OCR...")
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy file {image_path}")
        return ""
    
    # Tesseract nhận tên ngôn ngữ chuẩn như 'eng', 'vie', 'jpn'
    # Bạn có thể cần mapping từ mã ngôn ngữ của easyocr (như 'en', 'vi') sang tesseract ('eng', 'vie') nếu cần
    lang_mapping = {
        'en': 'eng',
        'vi': 'vie',
        'ja': 'jpn',
        'ko': 'kor',
        'zh': 'chi_sim'
    }
    
    tess_langs = [lang_mapping.get(l, l) for l in lang]
    lang_str = '+'.join(tess_langs)
    
    try:
        # Tải hình ảnh
        img = Image.open(image_path)
        
        # --- TIỀN XỬ LÝ ẢNH ĐỂ TĂNG ĐỘ CHÍNH XÁC ---
        # 1. Phóng to ảnh lên gấp 2-3 lần. Tesseract hoạt động tốt nhất khi text cao khoảng 30 pixel.
        width, height = img.size
        img = img.resize((width * 2, height * 2), Image.Resampling.LANCZOS)
        
        # 2. Chuyển ảnh sang thang độ xám (Grayscale) để giảm nhiễu màu
        img = img.convert('L')
        
        # Cấu hình Tesseract: 
        # --oem 3 (Sử dụng Default OCR Engine Mode)
        # --psm 6 (Assume a single uniform block of text - Giúp chữ cái ít bị rời rạc hay nhầm lẫn)
        custom_config = r'--oem 3 --psm 6'
        
        # Trích xuất văn bản
        extracted_text = pytesseract.image_to_string(img, lang=lang_str, config=custom_config)
        
        # Xử lý dọn dẹp văn bản (loại bỏ nhiều khoảng trắng hoặc newline dư thừa)
        extracted_text = re.sub(r'\s+', ' ', extracted_text).strip()
        
        print("\n--- KẾT QUẢ OCR ---")
        print(extracted_text if extracted_text else "(Không tìm thấy văn bản)")
        print("-------------------\n")
        return extracted_text
        
    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình OCR: {e}")
        # Gợi ý trong trường hợp tesseract chưa được cài đặt trong hệ thống (đặc biệt Windows)
        if "tesseract is not installed" in str(e).lower() or "not found" in str(e).lower():
            print("Lưu ý: Pytesseract yêu cầu công cụ Tesseract OCR đã được cài đặt trên hệ thống.")
            print("Bạn cần cài Tesseract (ví dụ: https://github.com/UB-Mannheim/tesseract/wiki) và")
            print("thêm đường dẫn của tesseract.exe vào biến môi trường PATH hoặc thiết lập bằng code:")
            print("pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'")
        return ""
