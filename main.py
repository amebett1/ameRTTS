import mss
import mss.tools
import easyocr
from deep_translator import GoogleTranslator
import os
import tkinter as tk
import time

CURRENT_REGION = {"top": 800, "left": 560, "width": 800, "height": 200}
should_select_region = False
is_selecting_region = False

class RegionSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-alpha", 0.3)
        self.root.attributes("-fullscreen", True)
        self.root.configure(background='black')
        self.root.attributes("-topmost", True)
        self.root.config(cursor="cross")

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.region = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", self.cancel)
        self.root.bind("<Button-3>", self.cancel)

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, 1, 1, outline='red', width=2, fill="gray")

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)
        
        if width > 10 and height > 10:
            self.region = {"top": top, "left": left, "width": width, "height": height}
        
        self.root.quit()
        self.root.destroy()

    def cancel(self, event=None):
        self.region = None
        self.root.quit()
        self.root.destroy()

def trigger_select_region():
    global should_select_region, is_selecting_region
    if not is_selecting_region:
        should_select_region = True

def do_select_region():
    global CURRENT_REGION
    print("\n--- Đang mở cửa sổ chọn vùng. Hãy kéo thả chuột để chọn (Nhấn Esc hoặc Chuột phải để hủy) ---")
    selector = RegionSelector()
    selector.root.mainloop()
    if selector.region:
        CURRENT_REGION = selector.region
        print(f"-> Đã cập nhật vùng chọn mới: {CURRENT_REGION}")
    else:
        print("-> Đã hủy chọn vùng.")

def capture_screen_region(output_filename="test.png"):
    """
    Bước 1: Chụp một vùng màn hình cố định.
    Giả sử màn hình có độ phân giải 1920x1080.
    Vùng chụp: Góc dưới cùng ở giữa (thường chứa phụ đề game).
    """
    print("Đang chụp màn hình...")
    with mss.mss() as sct:
        # Sử dụng tọa độ vùng chọn hiện tại
        monitor = CURRENT_REGION
        
        # Lấy dữ liệu màn hình
        sct_img = sct.grab(monitor)
        
        # Lưu thành file ảnh
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_filename)
        print(f"[Xong] Đã lưu ảnh màn hình vào: {output_filename}")
        return output_filename

def extract_text_from_image(image_path="test.png", lang=['en']):
    """
    Bước 2: Trích xuất văn bản (OCR).
    Sử dụng EasyOCR để đọc chữ từ file ảnh.
    """
    print("Đang trích xuất văn bản bằng EasyOCR...")
    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy file {image_path}")
        return ""

    # Khởi tạo EasyOCR reader với ngôn ngữ đã chọn
    # Lần đầu chạy có thể sẽ tốn thời gian tải model
    reader = easyocr.Reader(lang) 
    result = reader.readtext(image_path)
    
    # Kết quả trả về là list các tuple (bbox, text, confidence)
    extracted_text = " ".join([res[1] for res in result])
    print("\n--- KẾT QUẢ OCR ---")
    print(extracted_text if extracted_text else "(Không tìm thấy văn bản)")
    print("-------------------\n")
    
    return extracted_text

def translate_text(text, target_lang='vi'):
    """
    Bước 3: Dịch văn bản.
    Sử dụng deep-translator để dịch sang tiếng Việt.
    """
    if not text.strip():
        print("Không có chữ để dịch.")
        return

    print(f"Đang dịch sang ngôn ngữ '{target_lang}'...")
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        print("\n--- KẾT QUẢ DỊCH ---")
        print(translated)
        print("--------------------\n")
    except Exception as e:
        print(f"Lỗi khi dịch: {e}")

def run_pipeline():
    print("\n" + "="*30)
    print("=== BẮT ĐẦU DỊCH ===")
    
    # Bước 1
    img_path = capture_screen_region("test.png")
    
    # Bước 2 (Giả sử văn bản gốc là tiếng Anh)
    text = extract_text_from_image(img_path, lang=['en'])
    
    # Bước 3
    if text:
        translate_text(text, target_lang='vi')
    
    print("=== HOÀN THÀNH ===")
    print("="*30 + "\n")
    print("Đang chờ lệnh... (Nhấn 'Ctrl + Alt + Z' để dịch tiếp, 'Esc' để thoát)")

def main():
    import keyboard
    global should_select_region, is_selecting_region
    
    print("Khởi tạo phím tắt:")
    print("- Nhấn 'Ctrl + Alt + X' để kéo chọn vùng màn hình cần dịch.")
    print("- Nhấn 'Ctrl + Alt + Z' để bắt đầu chụp và dịch ngay.")
    print("- Nhấn 'Esc' để thoát chương trình.")
    print("\nĐang chờ lệnh...")
    
    # Đăng ký phím tắt
    keyboard.add_hotkey('ctrl+alt+z', run_pipeline)
    keyboard.add_hotkey('ctrl+alt+x', trigger_select_region)
    
    # Vòng lặp chính để xử lý UI tkinter an toàn trong luồng chính
    while True:
        if keyboard.is_pressed('esc'):
            print("Đã thoát chương trình.")
            break
            
        if should_select_region:
            should_select_region = False
            is_selecting_region = True
            
            # Tạm chờ để nhả phím
            time.sleep(0.3)
            do_select_region()
            
            # Reset lại trạng thái để tránh phím đè gây mở nhiều lần
            should_select_region = False
            is_selecting_region = False
            
        time.sleep(0.1)

if __name__ == "__main__":
    main()
