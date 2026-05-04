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
from datetime import datetime, timedelta

# အရောင်များ
w, g, y, r_clr, b = "\033[1;00m", "\033[1;32m", "\033[1;33m", "\033[1;31m", "\033[1;34m"
DEFAULT_GATEWAY = "192.168.110.1"
RAW_KEY_LINK = "https://raw.githubusercontent.com/heinminthant2022happy-bit/Aladdin/refs/heads/main/Cold.txt"

def Logo():
    os.system("clear")
    print(f"""{b}
    ___    __    ___    ____  ____  _____  _   __
   /   |  / /   /   |  / __ \/ __ \/  _/ |/ / / /
  / /| | / /   / /| | / / / / / / // / |   / / / 
 / ___ |/ /___/ ___ |/ /_/ / /_/ // / /   |/_/  
/_/  |_/_____/_/  |_/_____/_____/___//_/|_/(_)  
{g}           [ Ruijie Keep-Alive Tool ]{w}""")
    print(f"{y}" + "-"*45 + f"{w}")

def get_device_id():
    id_file = ".device_id"
    if os.path.exists(id_file): return open(id_file, "r").read().strip()
    try:
        serial = os.popen("getprop ro.serialno").read().strip()
        if not serial or len(serial) < 4:
            serial = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
        new_id = f"ALD-{serial.upper()}"
        with open(id_file, "w") as f: f.write(new_id)
        return new_id
    except: return "ALD-UNKNOWN-ID"

def get_network_time():
    """Google Server ထံမှ GMT အချိန်ကိုယူပြီး မြန်မာစံတော်ချိန်သို့ ပြောင်းသည်"""
    try:
        res = requests.get("https://www.google.com", timeout=5)
        gmt_str = res.headers.get('Date')
        gmt_dt = datetime.strptime(gmt_str, '%a, %d %b %Y %H:%M:%S %Z')
        # မြန်မာစံတော်ချိန် (GMT + 6:30)
        mm_time = gmt_dt + timedelta(hours=6, minutes=30)
        return mm_time
    except: return None

def parse_duration(duration_str):
    """စာသားထဲမှ ရက်၊ နာရီ၊ မိနစ်ကို ရှာသည်"""
    days = re.search(r'(\d+)\s*(d|day)', duration_str, re.I)
    hours = re.search(r'(\d+)\s*(h|hour)', duration_str, re.I)
    minutes = re.search(r'(\d+)\s*(m|min)', duration_str, re.I)
    d = int(days.group(1)) if days else 0
    h = int(hours.group(1)) if hours else 0
    m = int(minutes.group(1)) if minutes else 0
    return timedelta(days=d, hours=h, minutes=m)

def format_countdown(expiry_dt, current_dt):
    diff = expiry_dt - current_dt
    if diff.total_seconds() <= 0: return "Expired"
    days = diff.days
    hours, rem = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{days}D, {hours}H, {minutes}M, {seconds}S"

def check_online_license(user_key):
    dev_id = get_device_id()
    key_file = ".access_key"
    last_time_file = ".last_seen"
    
    net_time = get_network_time()
    curr_sys_time = datetime.now()

    # Time Tamper Protection
    if os.path.exists(last_time_file):
        try:
            last_ts = float(open(last_time_file, "r").read().strip())
            if curr_sys_time.timestamp() < last_ts:
                return False, "Time Travel Detected! Fix your date."
        except: pass
    
    current_working_time = net_time if net_time else curr_sys_time
    with open(last_time_file, "w") as f: f.write(str(current_working_time.timestamp()))

    try:
        res = requests.get(RAW_KEY_LINK, timeout=10)
        if res.status_code == 200:
            lines = res.text.splitlines()
            for line in lines:
                if "|" in line:
                    parts = [p.strip() for p in line.split("|")]
                    if parts[0] == dev_id and parts[1] == user_key:
                        raw_duration = parts[2]
                        
                        if os.path.exists(key_file):
                            saved_data = open(key_file, "r").read().strip().split("|")
                            expiry_dt = datetime.fromtimestamp(float(saved_data[1]))
                        else:
                            if not net_time: return None, "Activation requires internet!"
                            delta = parse_duration(raw_duration)
                            if delta.total_seconds() == 0: return False, "Invalid Duration!"
                            expiry_dt = net_time + delta
                            with open(key_file, "w") as f: f.write(f"{user_key}|{expiry_dt.timestamp()}")

                        if current_working_time < expiry_dt:
                            return True, expiry_dt
                        else:
                            if os.path.exists(key_file): os.remove(key_file)
                            return False, "Key Expired!"
            return False, "Key not found on Server!"
    except:
        if os.path.exists(key_file):
            try:
                s_key, s_exp_ts = open(key_file, "r").read().strip().split("|")
                expiry_dt = datetime.fromtimestamp(float(s_exp_ts))
                if curr_sys_time < expiry_dt: return True, expiry_dt
                else: return False, "Expired (Offline)"
            except: pass
        return None, "Connection Error!"
    return False, "Access Denied"

def license_screen():
    dev_id = get_device_id()
    key_file = ".access_key"
    while True:
        Logo()
        print(f"{w}[>] Device ID: {y}{dev_id}{w}")
        saved_key = ""
        if os.path.exists(key_file):
            try: saved_key = open(key_file, "r").read().strip().split("|")[0]
            except: pass
        
        user_key = saved_key if saved_key else input(f"{w}[?] Enter Access Key: {g}")
        if saved_key: print(f"{w}[*] Checking license...{w}")

        status, info = check_online_license(user_key)
        
        if status is True:
            remaining = format_countdown(info, datetime.now())
            print(f"{g}[+] Access Granted!{w}")
            print(f"{y}[!] Remaining: {remaining}{w}")
            time.sleep(2); break
        elif status is False:
            if os.path.exists(key_file): os.remove(key_file)
            print(f"{r_clr}[!] {info}{w}"); sys.exit()
        else:
            print(f"{y}[!] {info}{w}")
            if not saved_key: input(f"\n{g}Press Enter to retry...{w}")
            else: time.sleep(2); break

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
        raw_url = b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3dpZmlkb2c/c3RhZ2U9cG9ydGFsJmd3X2lkPTU4YjRiYmNiZmQwZCZnd19zbj1IMVU0MFNYMDExNTA3Jmd3X2FkZHJlc3M9MTkyLjE2OC45OS4xJmd3X3BvcnQ9MjA2MCZpcD0xOTIuMTY4Ljk5LjU0Jm1hYz0zYTpkZDo3ZTo2NDo4NzozNiZzbG90X251bT0xMyZuYXNpcD0xOTIuMTY4LjEuMTczJnNzaWQ9VkxBTjk5JnVzdGF0ZT0wJm1hY19yZXE9MSZ1cmw9aHR0cCUzQSUyRiUyRjE5Mi4xNjguMC4xJTJGJmNoYXBfaWQ9JTVDMzEwJmNoYXBfY2hhbGxlbmdlPSU1QzIxNiU1QzE2MCU1QzEyMiU1QzE3NyU1QzIxNyU1QzM2MCU1QzM2MyU1QzMyMSU1QzA1NiU1QzExMyU1QzIzMiU1QzIyMSU1QzMzMiU1QzI2MCU1QzI1MCU1QzAwMQ=='
        missing_padding = len(raw_url) % 4
        if missing_padding: raw_url += b'=' * (4 - missing_padding)
        try: self.session_url = base64.b64decode(raw_url).decode('utf-8', errors='ignore')
        except: self.session_url = None
        try: self.ip = open(".ip", "r").read().strip()
        except: self.ip = DEFAULT_GATEWAY

    async def keep_alive(self, expiry_dt):
        Logo()
        print(f"{g}[+] Internet Keep-Alive Running...{w}")
        async with aiohttp.ClientSession() as session:
            session_id = None
            while True:
                remaining = format_countdown(expiry_dt, datetime.now())
                if remaining == "Expired":
                    print(f"\n{r_clr}[!] Key Expired! Application Locked.{w}")
                    sys.exit()
                
                if not session_id: session_id = await get_session_id(session, self.session_url)
                if session_id:
                    params = {'token': session_id, 'phoneNumber': '09'+''.join(random.choice(string.digits) for _ in range(8))}
                    try:
                        async with session.post(f"http://{self.ip}:2060/wifidog/auth?", params=params, timeout=5) as res:
                            sys.stdout.write(f"\r{w}[{time.strftime('%H:%M:%S')}] Online | Left: {y}{remaining}{w}   ")
                            sys.stdout.flush()
                    except: session_id = None
                await asyncio.sleep(3)

def setup_process():
    Logo()
    print(f"{y}[*] Detecting Network...{w}")
    try:
        r = requests.get(f"http://{DEFAULT_GATEWAY}", timeout=5)
        match = re.search('gw_address=(.*?)&', r.url)
        if match:
            ip = match.group(1); open(".ip", "w").write(ip)
            print(f"{g}[+] Setup Success! IP: {ip}{w}")
        else:
            open(".ip", "w").write(DEFAULT_GATEWAY)
            print(f"{g}[+] Setup Success! (Default IP: {DEFAULT_GATEWAY}){w}")
    except: print(f"{r_clr}[!] Connection Failed!{w}")
    time.sleep(2)

def main():
    license_screen()
    while True:
        key_file = ".access_key"
        expiry_dt = datetime.now()
        if os.path.exists(key_file):
            try: expiry_dt = datetime.fromtimestamp(float(open(key_file, "r").read().strip().split("|")[1]))
            except: pass

        tool = AladdinTool(); Logo()
        print(f"{w}[1] Start Setup\n[2] Internet Keep-Alive\n{r_clr}[0] Exit")
        choice = input(f"\n{y}Select > {w}")
        if choice == '1': setup_process()
        elif choice == '2':
            try: asyncio.run(tool.keep_alive(expiry_dt))
            except KeyboardInterrupt: pass
        elif choice == '0': break

if __name__ == "__main__":
    main()

