import tkinter as tk
import queue
import ctypes
import config

command_queue = queue.Queue()

class RegionSelector:
    def __init__(self, parent_root=None):
        if parent_root:
            self.root = tk.Toplevel(parent_root)
        else:
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
        
        self.root.destroy()

    def cancel(self, event=None):
        self.region = None
        self.root.destroy()

def do_select_region(parent=None):
    print("\n--- Đang mở cửa sổ chọn vùng. Hãy kéo thả chuột để chọn (Nhấn Esc hoặc Chuột phải để hủy) ---")
    selector = RegionSelector(parent)
    if parent:
        parent.wait_window(selector.root)
    else:
        selector.root.mainloop()
        
    if selector.region:
        config.SETTINGS["region"] = selector.region
        config.save_config()
        print(f"-> Đã cập nhật vùng chọn mới: {config.SETTINGS['region']}")
    else:
        print("-> Đã hủy chọn vùng.")

class OverlayUI:
    def __init__(self, parent=None):
        if parent:
            self.root = tk.Toplevel(parent)
        else:
            self.root = tk.Tk()
            
        # Chỉnh màu đen thành trong suốt
        self.root.wm_attributes("-transparentcolor", "black")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg='black')
        
        # Thiết lập để Windows cho phép click xuyên qua lớp phủ
        try:
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED | WS_EX_TRANSPARENT)
        except Exception as e:
            print("Không thể thiết lập click-through:", e)

        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill='both', expand=True)
        
        self.hide_timer = None
        self.is_selecting = False
        self.check_queue()
        
    def check_queue(self):
        try:
            while True:
                msg, data = command_queue.get_nowait()
                if msg == "TRANSLATED":
                    self.show_text(data)
                elif msg == "SELECT_REGION":
                    if not self.is_selecting:
                        self.is_selecting = True
                        # Tạm ẩn overlay dịch
                        self.root.withdraw()
                        # Chạy UI chọn vùng
                        do_select_region(self.root)
                        # Hiển thị lại overlay dịch
                        self.root.deiconify()
                        self.is_selecting = False
                elif msg == "QUIT":
                    import os
                    os._exit(0)
        except queue.Empty:
            pass
        self.root.after(100, self.check_queue)
        
    def show_text(self, text):
        self.canvas.delete("all")
        if not text:
            return
            
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        
        # Hiển thị ở khoảng 1/5 màn hình tính từ dưới lên
        x = screen_w // 2
        y = screen_h - 150 
        
        font = ("Arial", 22, "bold") # Nhỏ hơn một chút cho gọn
        text_color = "white"
        box_color = "#202020" # Màu xám đậm (Solid), vì màu đen (#000000) bị làm trong suốt rồi
        
        # Giới hạn chiều rộng chữ khoảng 60% màn hình để tự động xuống dòng (gọn hơn)
        max_width = int(screen_w * 0.6)
        
        # Vẽ chữ trước để lấy kích thước (Bounding Box)
        text_id = self.canvas.create_text(x, y, text=text, font=font, fill=text_color, width=max_width, justify='center')
        
        # Lấy tọa độ hộp bao quanh chữ
        bbox = self.canvas.bbox(text_id)
        
        if bbox:
            padding_x = 25
            padding_y = 15
            # Vẽ hộp vuông bo quanh chữ
            rect_id = self.canvas.create_rectangle(
                bbox[0] - padding_x, bbox[1] - padding_y,
                bbox[2] + padding_x, bbox[3] + padding_y,
                fill=box_color, outline="", tags="bg_box"
            )
            # Đẩy hộp nền xuống dưới lớp chữ
            self.canvas.tag_lower(rect_id, text_id)
        
        # Tự động xóa chữ sau 7 giây
        if self.hide_timer:
            self.root.after_cancel(self.hide_timer)
        self.hide_timer = self.root.after(7000, lambda: self.canvas.delete("all"))
