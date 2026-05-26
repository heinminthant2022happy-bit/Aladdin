import os
import sys
import urllib.request

# ၁။ မိမိ၏ GitHub Repository လမ်းကြောင်းများ သတ်မှတ်ခြင်း
GITHUB_SO_URL = "https://raw.githubusercontent.com/heinminthant2022happy-bit/Aladdin/refs/heads/main/lucky.so"
LOCAL_SO_NAME = "lucky.so"

# ၂။ Android Restriction (dlopen) ကိုကျော်ရန်အတွက် .so ဖိုင်အား Termux ရဲ့ လုံခြုံသော Home Folder ထဲတွင်သာ ဆောက်ခြင်း
termux_home = os.path.expanduser("~")
local_so_path = os.path.join(termux_home, LOCAL_SO_NAME)

# ၃။ User အသုံးပြုရ လွယ်ကူစေရန် သန့်ရှင်းရေး ကြိုတင်လုပ်ခြင်း
if os.path.exists(local_so_path):
    try: os.remove(local_so_path)
    except: pass

print("\033[1;36m[*] Fetching secure core components from server...\033[0m")

# ၄။ GitHub ပေါ်မှ lucky.so ကို ခေတ္တယာယီ ဒေါင်းလုဒ်ဆွဲယူခြင်း
try:
    urllib.request.urlretrieve(GITHUB_SO_URL, local_so_path)
except Exception as e:
    print(f"\033[1;31m[!] Server Connection Error: Components များ ဒေါင်းလုဒ်ဆွဲ၍ မရပါ။\033[0m")
    print(f"Reason: {e}")
    sys.exit(1)

# ၅။ Python Module Path ထဲသို့ Termux Home လမ်းကြောင်းအား ထည့်သွင်းခြင်း
if termux_home not in sys.path:
    sys.path.insert(0, termux_home)

print("\033[1;32m[+] Components loaded successfully! Launching Tool...\033[0m\n")

# ၆။ Tool ကို စတင်ပွင့်စေပြီး၊ ပိတ်သွားပါက လုံခြုံရေးအရ .so ဖိုင်အား ချက်ချင်း ပြန်ဖျက်ခြင်း
try:
    import lucky
except Exception as e:
    print(f"\033[1;31m[!] Error: Tool အား Run ရန် ပျက်ကွက်ခဲ့ပါသည်။\033[0m")
    print(f"Reason: {e}")
finally:
    # ကုဒ်များ လုံခြုံရေးအတွက် Tool ပိတ်လိုက်သည်နှင့် .so ဖိုင်အား ဖုန်းထဲမှ အပြီးဖျက်ဆီးပစ်ခြင်း
    if os.path.exists(local_so_path):
        try: os.remove(local_so_path)
        except: pass
          
