from deep_translator import GoogleTranslator
import config

def translate_text(text):
    target_lang = config.SETTINGS["target_lang"]
    if not text.strip():
        print("Không có chữ để dịch.")
        return None

    print(f"Đang dịch sang ngôn ngữ '{target_lang}'...")
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        print("\n--- KẾT QUẢ DỊCH ---")
        print(translated)
        print("--------------------\n")
        return translated
    except Exception as e:
        print(f"Lỗi khi dịch: {e}")
        return None
