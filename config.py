import json
import os

CONFIG_FILE = "config.json"

SETTINGS = {
    "target_lang": "vi",
    "hotkey_translate": "ctrl+alt+z",
    "hotkey_crop": "ctrl+alt+x",
    "region": {"top": 800, "left": 560, "width": 800, "height": 200}
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                SETTINGS.update(data)
        except Exception as e:
            print(f"Lỗi đọc config: {e}")

def save_config():
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(SETTINGS, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Lỗi lưu config: {e}")

load_config()
