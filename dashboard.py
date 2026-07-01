import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import config

LANGUAGES = {
    "Tiếng Việt": "vi",
    "Tiếng Anh": "en",
    "Tiếng Trung (Giản thể)": "zh-CN",
    "Tiếng Nhật": "ja",
    "Tiếng Hàn": "ko"
}

class DashboardUI:
    def __init__(self, start_callback):
        self.root = tk.Tk()
        self.root.title("ameRTTS Dashboard")
        self.root.geometry("400x320")
        self.root.resizable(False, False)
        self.start_callback = start_callback
        
        self.create_widgets()
        
    def create_widgets(self):
        title_lbl = tk.Label(self.root, text="ameRTTS Control Panel", font=("Arial", 16, "bold"))
        title_lbl.pack(pady=15)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Kiểm tra hệ thống", width=25, command=self.check_system).pack(pady=5)
        tk.Button(btn_frame, text="Cài đặt", width=25, command=self.open_settings).pack(pady=5)
        
        self.start_btn = tk.Button(btn_frame, text="BẮT ĐẦU", width=25, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.start_app)
        self.start_btn.pack(pady=20)
        
        self.status_lbl = tk.Label(self.root, text="Sẵn sàng", fg="gray")
        self.status_lbl.pack(side="bottom", pady=10)

    def check_system(self):
        self.status_lbl.config(text="Đang kiểm tra kết nối...", fg="blue")
        self.root.update()
        
        try:
            urllib.request.urlopen('http://translate.google.com', timeout=3)
            internet_ok = True
        except:
            internet_ok = False
            
        if internet_ok:
            messagebox.showinfo("Thành công", "Kết nối mạng TỐT.\nHệ thống Google Translate sẵn sàng!")
            self.status_lbl.config(text="Hệ thống ổn định", fg="green")
        else:
            messagebox.showerror("Lỗi", "Không thể kết nối đến Google Translate. Vui lòng kiểm tra mạng!")
            self.status_lbl.config(text="Lỗi kết nối", fg="red")

    def open_settings(self):
        SettingsWindow(self.root)

    def start_app(self):
        self.start_btn.config(state="disabled", text="ĐANG CHẠY...")
        self.status_lbl.config(text="Ứng dụng đang chạy nền", fg="green")
        self.root.withdraw() # Ẩn dashboard
        self.start_callback(self.root)
        
class SettingsWindow:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Cài đặt")
        self.top.geometry("350x260")
        self.top.grab_set()
        
        tk.Label(self.top, text="Ngôn ngữ đích:").pack(pady=(15, 0))
        self.lang_var = tk.StringVar()
        current_lang_code = config.SETTINGS["target_lang"]
        
        current_lang_name = "Tiếng Việt"
        for name, code in LANGUAGES.items():
            if code == current_lang_code:
                current_lang_name = name
                break
                
        self.lang_combo = ttk.Combobox(self.top, textvariable=self.lang_var, values=list(LANGUAGES.keys()), state="readonly")
        self.lang_combo.set(current_lang_name)
        self.lang_combo.pack(pady=5)
        
        tk.Label(self.top, text="Phím tắt Dịch:").pack(pady=(10, 0))
        self.hotkey_trans_var = tk.StringVar(value=config.SETTINGS["hotkey_translate"])
        tk.Entry(self.top, textvariable=self.hotkey_trans_var).pack(pady=5)
        
        tk.Label(self.top, text="Phím tắt Chọn vùng:").pack(pady=(10, 0))
        self.hotkey_crop_var = tk.StringVar(value=config.SETTINGS["hotkey_crop"])
        tk.Entry(self.top, textvariable=self.hotkey_crop_var).pack(pady=5)
        
        tk.Button(self.top, text="Lưu & Đóng", bg="#2196F3", fg="white", command=self.save).pack(pady=15)
        
    def save(self):
        selected_name = self.lang_var.get()
        config.SETTINGS["target_lang"] = LANGUAGES.get(selected_name, "vi")
        config.SETTINGS["hotkey_translate"] = self.hotkey_trans_var.get()
        config.SETTINGS["hotkey_crop"] = self.hotkey_crop_var.get()
        
        config.save_config()
        messagebox.showinfo("Thành công", "Đã lưu cài đặt!\nThay đổi phím tắt sẽ có hiệu lực sau khi khởi động lại chương trình.")
        self.top.destroy()
