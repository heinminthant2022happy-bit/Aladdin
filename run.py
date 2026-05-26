import sys
import os

    # lucky.so ဖိုင်ကို လှမ်းခေါ် Run ခြင်း
    import lucky
except Exception as e:
    print(f"\033[1;31m[!] Error: Tool အလုပ်လုပ်ရန် lucky.so ဖိုင် လိုအပ်ပါသည်။\033[0m")
    print(f"Reason: {e}")
