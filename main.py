import keyboard
from capture import capture_screen_region
from ocr import extract_text_from_image
from translator import translate_text
from ui import OverlayUI, command_queue
import config
from dashboard import DashboardUI

def run_pipeline():
    print("\n" + "="*30)
    print("=== BẮT ĐẦU DỊCH ===")
    img_path = capture_screen_region("test.png")
    text = extract_text_from_image(img_path, lang=['en'])
    if text:
        translated = translate_text(text)
        if translated:
            command_queue.put(("TRANSLATED", translated))
    print("=== HOÀN THÀNH ===")
    print("="*30 + "\n")

def quit_app():
    print("Đang thoát chương trình...")
    import os
    os._exit(0)

def start_overlay(root):
    # Đăng ký phím tắt bằng thread riêng, dùng hotkey từ config
    keyboard.add_hotkey(config.SETTINGS["hotkey_translate"], run_pipeline)
    keyboard.add_hotkey(config.SETTINGS["hotkey_crop"], lambda: command_queue.put(("SELECT_REGION", None)))
    keyboard.add_hotkey('esc', quit_app)
    
    print(f"Phím tắt dịch: {config.SETTINGS['hotkey_translate']}")
    print(f"Phím tắt chọn vùng: {config.SETTINGS['hotkey_crop']}")
    print("\nChương trình Overlay UI đang chạy nền...")
    
    # Khởi chạy giao diện chính (OverlayUI là một Toplevel con của DashboardUI)
    app = OverlayUI(root)

def main():
    dashboard = DashboardUI(start_callback=start_overlay)
    dashboard.root.mainloop()

if __name__ == "__main__":
    main()
