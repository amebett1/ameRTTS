import mss
import mss.tools
import config

def capture_screen_region(output_filename="test.png"):
    print("Đang chụp màn hình...")
    with mss.mss() as sct:
        monitor = config.SETTINGS["region"]
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_filename)
        print(f"[Xong] Đã lưu ảnh màn hình vào: {output_filename}")
        return output_filename
