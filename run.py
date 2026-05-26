import sys
import os

# ဖုန်းရဲ့ Download Folder လမ်းကြောင်းကို သတ်မှတ်ခြင်း
storage_path = "/sdcard/Download"

if storage_path not in sys.path:
    sys.path.append(storage_path)

try:
    # lucky.so ဖိုင်ကို လှမ်းခေါ် Run ခြင်း
    import lucky
except Exception as e:
    print(f"\033[1;31m[!] Error: Tool အလုပ်လုပ်ရန် lucky.so ဖိုင် လိုအပ်ပါသည်။\033[0m")
    print(f"Reason: {e}")
