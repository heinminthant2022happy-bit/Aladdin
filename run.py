import os
import sys
import urllib.request
import asyncio

GITHUB_SO_URL = "https://raw.githubusercontent.com/heinminthant2022happy-bit/Aladdin/refs/heads/main/lucky.so"
LOCAL_SO_NAME = "lucky.so"

termux_home = os.path.expanduser("~")
local_so_path = os.path.join(termux_home, LOCAL_SO_NAME)

if os.path.exists(local_so_path):
    try: os.remove(local_so_path)
    except: pass

print("\033[1;36m[*] Fetching secure core components from server...\033[0m")

try:
    urllib.request.urlretrieve(GITHUB_SO_URL, local_so_path)
except Exception as e:
    print(f"\033[1;31m[!] Server Connection Error: Components များ ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။\033[0m")
    print(f"Reason: {e}")
    sys.exit(1)

if termux_home not in sys.path:
    sys.path.insert(0, termux_home)

print("\033[1;32m[+] Components loaded successfully! Launching Tool...\033[0m\n")

try:
    # lucky.so ကို import အရင်လုပ်သည်
    import lucky
    
    # ပြဿနာဖြေရှင်းရန် - lucky.so ထဲက main_loop() ကို တိုက်ရိုက် လှမ်း Run ခိုင်းခြင်း
    if hasattr(lucky, 'main_loop'):
        asyncio.run(lucky.main_loop())
    else:
        print("\033[1;31m[!] Error: lucky.main_loop ကို ရှာမတွေ့ပါ။\033[0m")
except Exception as e:
    print(f"\033[1;31m[!] Error: Tool အား Run ရန် ပျက်ကွက်ခဲ့ပါသည်။\033[0m")
    print(f"Reason: {e}")
finally:
    if os.path.exists(local_so_path):
        try: os.remove(local_so_path)
        except: pass

