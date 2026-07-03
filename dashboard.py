import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import urllib.request
import config

# Cấu hình giao diện tổng thể
ctk.set_appearance_mode("System")  # Hỗ trợ tự động Dark/Light mode theo Windows
ctk.set_default_color_theme("blue")

LANGUAGES = {
    "Tiếng Việt": "vi",
    "Tiếng Anh": "en",
    "Tiếng Trung (Giản thể)": "zh-CN",
    "Tiếng Nhật": "ja",
    "Tiếng Hàn": "ko"
}

class DashboardUI:
    def __init__(self, start_callback):
        self.root = ctk.CTk()
        self.root.title("AmeRTTS")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.start_callback = start_callback
        
        self.create_widgets()
        
    def create_widgets(self):
        # Tiêu đề với Font Roboto hiện đại
        title_lbl = ctk.CTkLabel(self.root, text="AmeRTTS", font=ctk.CTkFont(family="Roboto", size=24, weight="bold"))
        title_lbl.pack(pady=(25, 20))
        
        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        # Nút phụ (Secondary) - Thiết kế Outline
        ctk.CTkButton(btn_frame, text="Kiểm tra hệ thống", width=220, height=35,
                      fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                      command=self.check_system).pack(pady=8)
                      
        ctk.CTkButton(btn_frame, text="Cài đặt", width=220, height=35,
                      fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),
                      command=self.open_settings).pack(pady=8)
        
        # Nút chính (Primary) - Thiết kế Solid nền xanh
        self.start_btn = ctk.CTkButton(btn_frame, text="BẮT ĐẦU", width=220, height=45, 
                                       font=ctk.CTkFont(size=16, weight="bold"),
                                       fg_color="#10B981", hover_color="#059669", # Xanh lá hiện đại
                                       command=self.start_app)
        self.start_btn.pack(pady=(20, 10))
        
        # Trạng thái
        self.status_lbl = ctk.CTkLabel(self.root, text="🟢 Sẵn sàng", font=ctk.CTkFont(size=12), text_color="gray")
        self.status_lbl.pack(side="bottom", pady=10)

    def check_system(self):
        self.status_lbl.configure(text="🔵 Đang kiểm tra kết nối...", text_color="#3B82F6")
        self.root.update()
        
        try:
            urllib.request.urlopen('http://translate.google.com', timeout=3)
            internet_ok = True
        except:
            internet_ok = False
            
        if internet_ok:
            messagebox.showinfo("Thành công", "Kết nối mạng TỐT.\nHệ thống Google Translate sẵn sàng!")
            self.status_lbl.configure(text="🟢 Hệ thống ổn định", text_color="#10B981")
        else:
            messagebox.showerror("Lỗi", "Không thể kết nối đến Google Translate. Vui lòng kiểm tra mạng!")
            self.status_lbl.configure(text="🔴 Lỗi kết nối", text_color="#EF4444")

    def open_settings(self):
        SettingsWindow(self.root)

    def start_app(self):
        self.start_btn.configure(state="disabled", text="⏳ ĐANG CHẠY...")
        self.status_lbl.configure(text="🟢 Ứng dụng đang chạy nền", text_color="#10B981")
        self.root.withdraw() # Ẩn dashboard
        self.start_callback(self.root)
        
class SettingsWindow:
    def __init__(self, parent):
        self.top = ctk.CTkToplevel(parent)
        self.top.title("Cài đặt")
        self.top.geometry("380x320")
        self.top.attributes("-topmost", True)
        self.top.grab_set() # Block main window
        
        # Lang
        ctk.CTkLabel(self.top, text="Ngôn ngữ đích:").pack(pady=(20, 5))
        self.lang_var = ctk.StringVar()
        current_lang_code = config.SETTINGS["target_lang"]
        
        current_lang_name = "Tiếng Việt"
        for name, code in LANGUAGES.items():
            if code == current_lang_code:
                current_lang_name = name
                break
                
        self.lang_combo = ctk.CTkComboBox(self.top, variable=self.lang_var, values=list(LANGUAGES.keys()), width=250)
        self.lang_combo.set(current_lang_name)
        self.lang_combo.pack(pady=5)
        
        # Hotkey Translate
        ctk.CTkLabel(self.top, text="Phím tắt Dịch:").pack(pady=(10, 5))
        self.hotkey_trans_var = ctk.StringVar(value=config.SETTINGS["hotkey_translate"])
        ctk.CTkEntry(self.top, textvariable=self.hotkey_trans_var, width=250).pack(pady=5)
        
        # Hotkey Crop
        ctk.CTkLabel(self.top, text="Phím tắt Chọn vùng:").pack(pady=(10, 5))
        self.hotkey_crop_var = ctk.StringVar(value=config.SETTINGS["hotkey_crop"])
        ctk.CTkEntry(self.top, textvariable=self.hotkey_crop_var, width=250).pack(pady=5)
        
        # Save Button
        ctk.CTkButton(self.top, text="Lưu & Đóng", fg_color="#3B82F6", hover_color="#2563EB", command=self.save, width=200).pack(pady=(25, 15))
        
    def save(self):
        selected_name = self.lang_var.get()
        config.SETTINGS["target_lang"] = LANGUAGES.get(selected_name, "vi")
        config.SETTINGS["hotkey_translate"] = self.hotkey_trans_var.get()
        config.SETTINGS["hotkey_crop"] = self.hotkey_crop_var.get()
        
        config.save_config()
        messagebox.showinfo("Thành công", "Đã lưu cài đặt!\nThay đổi phím tắt sẽ có hiệu lực sau khi khởi động lại chương trình.")
        self.top.destroy()
