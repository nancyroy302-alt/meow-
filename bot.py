import os
import sys
import re
import requests
import json
import time
import random
import uuid
import getpass
import base64
import threading
import subprocess
import hashlib
import platform  
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============= WINDOWS COMPATIBILITY FIXES =============
# ANSI colors for Windows CMD/PowerShell
if platform.system() == "Windows":
    os.system('color')
    
# ============= NEON PINK & PURE WHITE THEME =============
class colors:
    # Hot Neon Pink Theme - Main color scheme (SUPER BRIGHT)
    PINK = '\033[38;5;206m'        # Bright Neon Pink
    BPINK = '\033[1;38;5;206m'     # Bold Neon Pink
    LIGHT_PINK = '\033[38;5;219m'   # Very Light Pink
    DARK_PINK = '\033[38;5;163m'    # Darker Pink
    
    # White Shades
    WHITE = '\033[0;37m'
    BWHITE = '\033[1;37m'
    BRIGHT_WHITE = '\033[1;97m'
    
    # Status Colors (Original logic colors, made brighter)
    GREEN = '\033[1;32m'
    RED = '\033[1;31m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[1;34m'
    MAGENTA = '\033[1;35m'
    CYAN = '\033[1;36m'
    
    # Bold Status Colors
    BGREEN = '\033[1;32m'
    BRED = '\033[1;31m'
    BYELLOW = '\033[1;33m'
    BCYAN = '\033[1;36m'
    
    # Background Colors
    BG_BLACK = '\033[40m'
    BG_PINK = '\033[48;5;206m'
    BG_WHITE = '\033[47m'
    
    # Reset
    RESET = '\033[0m'
    
    # Icons (Original icons retained)
    CHECK = '✓'
    CROSS = '✗'
    ARROW = '→'
    STAR = '★'
    HEART = '♥'
    DIAMOND = '♦'
    BULLET = '•'
    BOX = '■'
    CIRCLE = '●'

# Global variables (EXACTLY AS IN ORIGINAL SCRIPT)
user_data = {
    'cookies': [],
    'cookie_data': {},
    'preprocessing_done': False,
    'blocked_cookies': set(),
    'success_count': 0,
    'fail_count': 0,
    'total_target': 0,
    'is_running': False,
    'comment_logs': [],
    'current_round': 1,
    'total_rounds': 1,
    'settings': {},
    'start_time': None,
    'round_start_time': None,
    'speed_history': []
}

# Headers (EXACTLY AS IN ORIGINAL SCRIPT)
headget = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'dpr': '1',
    'priority': 'u=0, i',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.100", "Chromium";v="127.0.6533.100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'viewport-width': '795',
}

headpost = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://web.facebook.com',
    'priority': 'u=1, i',
    'referer': 'https://web.facebook.com/',
    'sec-ch-prefers-color-scheme': 'light',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-full-version-list': '"Not)A;Brand";v="99.0.0.0", "Google Chrome";v="127.0.6533.99", "Chromium";v="127.0.6533.99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'x-asbd-id': '129477',
}

def clear_screen():
    """Clear terminal screen - Windows compatible"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_box(text, color=colors.PINK, width=60):
    """Print text in a beautiful box with neon pink theme"""
    lines = text.split('\n')
    # Use standard ASCII borders to avoid terminal display issues
    top_border = color + "+-" + "-" * width + "-+" + colors.RESET
    bottom_border = color + "+-" + "-" * width + "-+" + colors.RESET
    
    print(top_border)
    for line in lines:
        # Proper padding to match width
        content = line + " " * (width - len(line))
        print(color + "| " + colors.BWHITE + content + color + " |" + colors.RESET)
    print(bottom_border)

def print_header(text, color=colors.BPINK):
    """Print a beautiful header with neon pink"""
    print(f"\n{color}{'═' * 70}{colors.RESET}")
    print(f"{color}   {colors.BWHITE}{text}{colors.RESET}")
    print(f"{color}{'═' * 70}{colors.RESET}")

def print_success(text):
    """Print success message"""
    print(f"  {colors.BGREEN}{colors.CHECK}{colors.RESET} {colors.GREEN}{text}{colors.RESET}")

def print_error(text):
    """Print error message"""
    print(f"  {colors.BRED}{colors.CROSS}{colors.RESET} {colors.RED}{text}{colors.RESET}")

def print_info(text):
    """Print info message with neon pink bullet"""
    print(f"  {colors.BPINK}{colors.HEART}{colors.RESET} {colors.BWHITE}{text}{colors.RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"  {colors.BYELLOW}{colors.STAR}{colors.RESET} {colors.YELLOW}{text}{colors.RESET}")

def print_progress_bar(current, total, bar_length=40):
    """Print a beautiful progress bar with neon pink theme"""
    percent = current / total if total > 0 else 0
    filled = int(bar_length * percent)
    bar = f"{colors.BG_PINK}{'█' * filled}{colors.RESET}{colors.BWHITE}{'░' * (bar_length - filled)}{colors.RESET}"
    print(f"  {bar} {colors.BPINK}{current}/{total}{colors.RESET} ({percent*100:.1f}%)")

def print_banner():
    """Print premium tool banner with neon pink & white theme"""
    banner = f"""{colors.BPINK}
░█████╗░███████╗████████╗{colors.WHITE}░█████╗░██████╗░
{colors.BPINK}██╔══██╗██╔════╝╚══██╔══╝{colors.WHITE}██╔══██╗██╔══██╗
{colors.BPINK}███████║█████╗░░░░░██║░░░{colors.WHITE}███████║██████╦╝
{colors.BPINK}██╔══██║██╔══╝░░░░░██║░░░{colors.WHITE}██╔══██║██╔══██╗
{colors.BPINK}██║░░██║██║░░░░░░░░██║░░░{colors.WHITE}██║░░██║██████╦╝
{colors.BPINK}╚═╝░░╚═╝╚═╝░░░░░░░░╚═╝░░░{colors.WHITE}╚═╝░░╚═╝╚═════╝░
    {colors.BWHITE}⚡ {colors.BPINK}AFTAB SHEIKH AUTO VOTING PRO v2 - SPEED X EMOJI {colors.BWHITE}⚡
    """
    print(banner)

def get_unique_id():
    """Get unique ID - Windows compatible"""
    # For Windows, use machine GUID
    try:
        if platform.system() == "Windows":
            import wmi
            c = wmi.WMI()
            for system in c.Win32_ComputerSystemProduct():
                return system.UUID
    except:
        pass
    
    # Fallback: Use Windows username + computer name
    try:
        import socket
        return f"{os.environ.get('COMPUTERNAME', 'PC')}-{os.environ.get('USERNAME', 'USER')}"
    except:
        return "WINDOWS-USER-99"

def Privacy():
    secret_salt = "JATIIIN"
    
    # Generating Unique Key
    device_id = get_unique_id()
    raw_data = f"{device_id}|{secret_salt}"
    hash_object = hashlib.sha256(raw_data.encode()).hexdigest().upper()
    
    # Final Formatting (XXXX-XXXX-XXXX-XXXX)
    final_key = "-".join([hash_object[i:i+4] for i in range(0, 20, 4)])
    url = "https://pastebin.com/raw/AZFZMw42"

    print(f"{colors.PINK}╔{'═'*58}╗{colors.RESET}")
    
    try:
        response = requests.get(url, timeout=10).text.strip().upper()
        
        if final_key in response: 
            print(f"{colors.PINK}║ {colors.BGREEN}            [[=== ACCESS APPROVED BY AFTAB ===]]             {colors.PINK}║")
            print(f"{colors.PINK}╚{'═'*58}╝{colors.RESET}")
        else:
            print(f"{colors.PINK}║ {colors.BRED}          [[== ACCESS NOT APPROVED ==]]                  {colors.PINK}║")
            print(f"{colors.PINK}║ {colors.BWHITE} Your Key: {colors.BYELLOW}{final_key:<45} {colors.PINK}║")
            print(f"{colors.PINK}╚{'═'*58}╝{colors.RESET}")
            # Key copy karne ka option (Bonus)
            print(f"\n{colors.BYELLOW}Hint: Copy your key and send it to the admin!{colors.RESET}")
            sys.exit()
            
    except Exception:
        print(f"{colors.PINK}║ {colors.BRED}          [[== CHECK YOUR INTERNET CONNECTION ==]]         {colors.PINK}║")
        print(f"{colors.PINK}╚{'═'*58}╝{colors.RESET}")
        sys.exit()
            
    except Exception:
        print(f"{colors.PINK}║ {colors.BRED}            [[== NO INTERNET CONNECTION ==]]               {colors.PINK}║")
        print(f"{colors.PINK}╚{'═'*58}╝{colors.RESET}")
        sys.exit()
        
        
def format_time(seconds):
    """Format time in human readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds // 60
        secs = seconds % 60
        return f"{int(minutes)}m {int(secs)}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"

def calculate_speed(count, elapsed):
    """Calculate comments per minute speed"""
    if elapsed == 0:
        return 0
    return (count / elapsed) * 60

def add_emoji_to_comment(text, use_emoji):
    """Add random emoji to comment"""
    if not use_emoji:
        return text
    emojis = ["😀","😂","🔥","❤️","👍","✨","😎","🚀","💯","😍","🩷","🩵","👿","💀","⚡","🩶","💋","👅","☄️","🏴‍☠️","♥️","💞","💜","👽","🎃","😡","🥺","😘","🦠","😈","🧸","💸","🙈","🪺","💕","💥","😝","🇹🇩","🇻🇳","🇸🇪","🚩","🎀","🎈","🤷🏻","🥀","🎧","🧿","♋","🔱","🇩🇬","💌","💡","💵","🌊","🦞","🍫","🍰","🗿","🏆","🔵","🟣","🔴","🔞","🚭","🛐","🧡","🪼","🐦‍🔥","🐷","⛈️","🌤️","💃🏻","🧛🏻","🧚🏻","⛹🏻","🤸🏻","🧘🏻","🇾🇪","✝️","🈴","♒","💎","🔮","🦾","🎭","🎪","🎰","🎮","🕹️","🎯","🎲","🧩","🦄","🐉","🦖","🦂","🦁","🐯","🐼","🐨","👑","🎩","💍","💼","🩸","🧠","🦷","🧬","🧪","🌋","🌪️","🌈","☀️","🌙","⭐","🍀","🍁","🍄","🥑","🍕","🍔","🍟","🌮","🍣","🍦","🍩","🍷","🍹","🍺","🌍","🗺️","🏔️","🌅","🌉","✈️","🛸","🚁","🏎️","🚜","⏰","⏳","🔋","💻","📱","📡","🔑","🔒","🔔","📣","📦","📜","📂","📈","📌","📍","⚔️","🛡️","🚬","⚰️","🪦","📿","🕉️","☪️","🔯","⛎","📳","💤","⚠️","🏁","🏴","🇦🇺","🇧🇷","🇨🇦","🇫🇷","🥳","🤩","🥰","🤤","🤠","🤡","🤥","🤫","🤭","🧐","🤓","😈","👹","👺","👻","👽","👾","🤖","😺","😸","😹","😻","😼","😽","🐶","🐱","🐭","🐹","🐰","🦊","🐻","🐼","🐻‍❄️","🐨","🐯","🦁","🐮","🐷","🐽","🐸","🐵","🙈","🙉","🙊","🐒","🐔","🐧","🐦","🐤","🐣","🐥","🦆","🦢","🦉","🦤","🪶","🦩","🦁","🐯","🦒","🐘","🦏","🦛","🐭","🐹","🐰","🐿️","🦫","🦔","🦇","🦦","🦥","🦘","🦬","🐄","🐖","🐏","🐑","🐐","🦌","🐎","🐆","🐅","🐃","🐂","🐫","🐪","🦙","🐘","🦣","🦏","🦛","🦒","🐒","🦍","🦧","🐕","🐩","🦮","🐕‍🦺","🐈","🐈‍⬛","🐆","🐅","🐊","🐢","🦎","🐍","🐲","🐉","🦕","🦖","🐳","🐋","🐬","🦭","🐟","🐠","🐡","🦈","🐙","🐚","🐌","🦋","🐛","🐜","🐝","🪲","🐞","🦗","🕷️","🕸️","🦂","🦟","🪰","🪱","🦠","💐","🌸","💮","🏵️","🌹","🥀","🌺","🌻","🌼","🌷","🌱","🪴","🌲","🌳","🌴","🌵","🌾","🌿","☘️","🍀","🍁","🍂","🍃","🍄","🐚","🪨","🪵","🍇","🍈","🍉","🍊","🍋","🍌","🍍","🥭","🍎","🍏","🍐","🍑","🍒","🍓","🫐","🥝","🍅","🫒","🥥","🥑","🍆","🥔","🥕","🌽","🌶️","🫑","🥒","🥬","🥦","🧄","🧅","🥜","🫘","🥐","🍞","🥖","🫓","🥨","🥯","🥞","🧇","🧀","🍖","🍗","🥩","🥓","🍔","🍟","🍕","🌭","🥪","🌮","🌯","🫔","🥙","🧆","🥚","🍳","🥘","🍲","🥣","🥗","🍿","🧈","🧂","🥫","🍱","🍘","🍙","🍚","🍛","🍜","🍝","🍠","🍢","🍣","🍤","🍥","🥮","🍡","🥟","🥠","🥡","🍦","🍧","🍨","🍩","🍪","🎂","🍰","🧁","🥧","🍫","🍬","🍭","🍮","🍯","🍼","🥛","☕","🫖","🍵","🍶","🍾","🍷","🍸","🍹","🍺","🍻","🥂","🥃","🥤","🧋","🧃","🧉","🧊"]
    return f"{text} {random.choice(emojis)}"

# ============= ALL ORIGINAL FUNCTIONS (LOGIC UNTOUCHED) =============

def datapoll(req, actor):
    """Extract tokens from Facebook response"""
    try:
        __a = str(random.randrange(1, 6))
        __hs = re.search('"haste_session":"(.*?)"', str(req)).group(1)
        __ccg = re.search('"connectionClass":"(.*?)"', str(req)).group(1)
        __rev = re.search('"__spin_r":(.*?),', str(req)).group(1)
        __spin_b = re.search('"__spin_b":"(.*?)"', str(req)).group(1)
        __spin_t = re.search('"__spin_t":(.*?),', str(req)).group(1)
        __hsi = re.search('"hsi":"(.*?)"', str(req)).group(1)
        fb_dtsg = re.search(r'"DTSGInitialData",\[],{"token":"(.*?)"}', str(req)).group(1)
        jazoest = re.search('jazoest=(.*?)"', str(req)).group(1)
        lsd = re.search(r'"LSD",\[],{"token":"(.*?)"}', str(req)).group(1)
        return {'av': actor, '__aaid': '0', '__user': actor, '__a': __a, '__hs': __hs, 'dpr': '2', '__ccg': __ccg, '__rev': __rev, '__hsi': __hsi, '__comet_req': '15', 'fb_dtsg': fb_dtsg, 'jazoest': jazoest, 'lsd': lsd, '__spin_r': __rev, '__spin_b': __spin_b, '__spin_t': __spin_t}
    except Exception as e:
        print_error(f"Failed to extract tokens: {e}")
        return None

def preprocess_cookies():
    """Pre-process all cookies - fetch tokens and pages"""
    global user_data
    
    cookies = user_data['cookies']
    total = len(cookies)
    processed = 0
    valid_count = 0
    
    print_header("🔍 COOKIE PRE-PROCESSING", colors.BPINK)
    print_info(f"Processing {total} cookies...")
    print()
    
    for i, cookie in enumerate(cookies, 1):
        try:
            # Progress indicator
            progress = f"  {colors.BWHITE}[{colors.BG_PINK}{'█' * int((i/total)*20)}{colors.BWHITE}{'░' * (20 - int((i/total)*20))}{colors.BWHITE}] {i}/{total}{colors.RESET}"
            sys.stdout.write(f"\r{progress}")
            sys.stdout.flush()
            
            req = requests.get('https://web.facebook.com/pages/?category=your_pages',
                               cookies={'cookie': cookie}, headers=headget, timeout=10)
            
            if req.status_code != 200:
                user_data['cookie_data'][cookie] = {'valid': False, 'error': f'HTTP {req.status_code}'}
                processed += 1
                continue

            data = datapoll(req.text, None)
            if not data:
                user_data['cookie_data'][cookie] = {'valid': False, 'error': 'Token extraction failed'}
                processed += 1
                continue

            actor_match = re.search(r'c_user=(\d+)', cookie)
            if not actor_match:
                user_data['cookie_data'][cookie] = {'valid': False, 'error': 'No c_user in cookie'}
                processed += 1
                continue
                
            actor_id = actor_match.group(1)

            # Extract pages info
            pages_info = []
            page_pattern = r'"page":{"name":"(.*?)","id":"(\d+?)"'
            page_matches = re.findall(page_pattern, str(req.text))
            
            if page_matches:
                pages_info = [(pid, pname) for pname, pid in page_matches]
            else:
                pages_info = re.findall(r'"is_profile_plus":.*?,"id":"(\d+)","name":"(.*?)"', str(req.text))

            data['av'] = actor_id
            data['__user'] = actor_id

            user_data['cookie_data'][cookie] = {
                'valid': True,
                'actor_id': actor_id,
                'data': data,
                'pages': pages_info[:5]
            }
            valid_count += 1

        except Exception as e:
            user_data['cookie_data'][cookie] = {'valid': False, 'error': str(e)[:50]}
        finally:
            processed += 1
    
    print("\n")
    print_box(f"✅ PRE-PROCESSING COMPLETE\n\nValid Cookies: {valid_count}/{total}\nSuccess Rate: {(valid_count/total*100):.1f}%", colors.BPINK)
    user_data['preprocessing_done'] = True

def load_cookies_from_file():
    """Load cookies from file - Windows compatible paths"""
    global user_data
    
    print_header("📁 COOKIE FILE LOADING", colors.BPINK)
    print_info("Enter path to cookie file:")
    print(f"  {colors.LIGHT_PINK}Examples:{colors.RESET} C:\\Users\\YourName\\Desktop\\cookies.txt, cookies.txt")
    print()
    
    file_path = input(f"  {colors.BPINK}➤{colors.RESET} ").strip()
    
    # Windows path handling
    if platform.system() == "Windows":
        # Remove quotes if user pasted with quotes
        file_path = file_path.strip('"').strip("'")
    
    if not os.path.exists(file_path):
        # Try relative path
        if not os.path.exists(file_path):
            print_error(f"File not found: {file_path}")
            return False
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        cookies = content.splitlines()
        cookies = [c.strip() for c in cookies if c.strip() and 'c_user=' in c]
        
        if not cookies:
            print_error("No valid cookies found in file!")
            return False
        
        user_data['cookies'] = cookies
        user_data['cookie_data'] = {}
        user_data['preprocessing_done'] = False
        user_data['blocked_cookies'] = set()
        
        print_success(f"Loaded {len(cookies)} cookies")
        return True
        
    except Exception as e:
        print_error(f"Error reading file: {e}")
        return False

def get_post_id(link):
    """Extract post ID from link"""
    try:
        if 'posts/' in link:
            match = re.search(r'posts/(\d+)', link)
            if match:
                return match.group(1)
        elif 'videos/' in link:
            match = re.search(r'videos/(\d+)', link)
            if match:
                return match.group(1)
        elif 'fbid=' in link:
            match = re.search(r'fbid=(\d+)', link)
            if match:
                return match.group(1)
        elif 'permalink.php?story_fbid=' in link:
            match = re.search(r'story_fbid=(\d+)', link)
            if match:
                return match.group(1)
        elif re.match(r'^\d+$', link):
            return link
    except:
        pass
    
    try:
        if 'facebook.com' in link or 'fb.com' in link:
            for cookie, data in user_data['cookie_data'].items():
                if data.get('valid', False):
                    req = requests.get(link, cookies={'cookie': cookie}, headers=headget, timeout=10)
                    match = re.search(r'"post_id":"(\d+)",', str(req.text))
                    if match:
                        return match.group(1)
    except:
        pass
    
    return None

def submit_comment(cookie, actor_id, post_id, text, data, doc_id, name, use_emoji, is_page=False):
    """Submit a single comment"""
    try:
        final_text = add_emoji_to_comment(text, use_emoji)
        feedback_id = base64.b64encode(f"feedback:{post_id}".encode("utf-8")).decode("utf-8")
        client_mutation_id = str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        
        variables = '{"feedLocation":"NEWSFEED","feedbackSource":1,"groupID":null,"input":{"client_mutation_id":"1","actor_id":"'+str(actor_id)+'","attachments":null,"feedback_id":"'+str(feedback_id)+'","formatting_style":null,"message":{"ranges":[],"text":"'+str(final_text)+'"},"attribution_id_v2":"CometHomeRoot.react,comet.home,via_cold_start,1714719369269,565120,4748854339,,","vod_video_timestamp":null,"is_tracking_encrypted":true,"tracking":[null],"feedback_source":"NEWS_FEED","idempotence_token":"client:'+str(client_mutation_id)+'","session_id":"'+str(session_id)+'"},"inviteShortLinkKey":null,"renderLocation":null,"scale":1,"useDefaultActor":false,"focusCommentID":null}'
        
        post_data = data.copy()
        post_data.update({
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'useCometUFICreateCommentMutation',
            'variables': variables,
            'server_timestamps': 'true',
            'doc_id': doc_id
        })
        
        curr_headers = headpost.copy()
        curr_headers.update({
            'x-fb-lsd': data['lsd'],
            'x-fb-friendly-name': 'useCometUFICreateCommentMutation'
        })
        
        req_cookies = {'cookie': cookie}
        if is_page:
            req_cookies = {'cookie': cookie + f';i_user={actor_id}'}
        
        resp = requests.post('https://web.facebook.com/api/graphql/', 
                            data=post_data, headers=curr_headers, 
                            cookies=req_cookies, timeout=15)
        
        if 'errorSummary' not in resp.text and '"id"' in resp.text:
            return True, "Success", name, actor_id, is_page
        else:
            error_msg = "Blocked" if "block" in resp.text.lower() else "Failed"
            return False, error_msg, name, actor_id, is_page
                    
    except Exception as e:
        return False, str(e)[:30], name, actor_id, is_page

def get_user_inputs():
    """Get all inputs from user (Auto Calculate Per ID Limit)"""
    print_header("⚙️ CONFIGURATION SETUP", colors.BPINK)
    
    # Comment text
    print_info("Enter your comment text:")
    comment_text = input(f"  {colors.BPINK}✎{colors.RESET} ").strip()
    if not comment_text:
        print_error("Comment text cannot be empty!")
        return None
    
    # Emoji choice
    print()
    print_info("Add random emojis?")
    print(f"  {colors.BGREEN}[y]{colors.RESET} Yes")
    print(f"  {colors.BRED}[n]{colors.RESET} No")
    emoji_choice = input(f"  {colors.BPINK}➤{colors.RESET} ").strip().lower()
    use_emoji = emoji_choice in ['y', 'yes']
    
    # Target count (ONLY TOTAL TARGET)
    print()
    print_info("Total comments target:")
    try:
        target = int(input(f"  {colors.BPINK}➤{colors.RESET} ").strip())
        if target <= 0:
            print_error("Target must be positive!")
            return None
    except ValueError:
        print_error("Invalid number!")
        return None
    
    # Mode selection
    print()
    print_info("Select commenting mode:")
    print(f"  {colors.BGREEN}[1]{colors.RESET} Only IDs")
    print(f"  {colors.BGREEN}[2]{colors.RESET} IDs + Pages")
    print(f"  {colors.BGREEN}[3]{colors.RESET} Only Pages")
    mode = input(f"  {colors.BPINK}➤{colors.RESET} ").strip()
    if mode not in ['1', '2', '3']:
        print_error("Invalid mode!")
        return None
    
    # Post link/ID
    print()
    print_info("Enter post link or post ID:")
    post_input = input(f"  {colors.BPINK}➤{colors.RESET} ").strip()
    
    print()
    print_info("Getting post ID...")
    post_id = get_post_id(post_input)
    
    if not post_id:
        print_error("Could not extract post ID!")
        return None
    
    print_success(f"Post ID: {post_id}")
    
    settings = {
        'comment_text': comment_text,
        'use_emoji': use_emoji,
        'target_total': target,
        'mode': mode,
        'post_id': post_id
    }
    
    return settings

def run_commenting(settings):
    """Main commenting function with AUTO-CALCULATED per ID limit"""
    global user_data
    
    if not user_data['preprocessing_done']:
        print_error("Please pre-process cookies first!")
        return False
    
    user_data.update(settings)
    user_data['is_running'] = True
    user_data['success_count'] = 0
    user_data['fail_count'] = 0
    user_data['comment_logs'] = []
    user_data['round_start_time'] = time.time()
    
    # Collect valid cookies
    active_cookies = []
    cookie_info = {}
    
    for cookie, data in user_data['cookie_data'].items():
        if data.get('valid', False) and cookie not in user_data.get('blocked_cookies', set()):
            active_cookies.append(cookie)
            cookie_info[cookie] = data
    
    if not active_cookies:
        print_error("No valid cookies found!")
        user_data['is_running'] = False
        return False
    
    # Calculate total available actors (IDs + Pages)
    total_actors = 0
    actor_details = []
    
    for cookie in active_cookies:
        data = cookie_info[cookie]
        actor_id = data['actor_id']
        pages_info = data.get('pages', [])
        
        # Add main account if mode allows
        if settings['mode'] in ['1', '2']:
            total_actors += 1
            actor_details.append({
                'cookie': cookie,
                'actor_id': actor_id,
                'data': data['data'],
                'type': 'account',
                'name': f"Account_{actor_id[-6:]}"
            })
        
        # Add pages if mode allows
        if settings['mode'] in ['2', '3'] and pages_info:
            for pid, pname in pages_info:
                total_actors += 1
                p_data = data['data'].copy()
                p_data['av'] = pid
                p_data['__user'] = pid
                actor_details.append({
                    'cookie': cookie,
                    'actor_id': pid,
                    'data': p_data,
                    'type': 'page',
                    'name': f"Page_{pname[:15]}"
                })
    
    # AUTO-CALCULATE per ID limit
    if total_actors == 0:
        print_error("No actors (IDs or pages) available!")
        return False
    
    # Calculate base limit (floor division)
    base_limit = settings['target_total'] // total_actors
    remainder = settings['target_total'] % total_actors
    
    print_header(f"🎯 ROUND {user_data['current_round']} STARTED", colors.BPINK)
    
    # Show configuration with auto-calculated values
    config_text = f"""TARGET: {settings['target_total']} comments
MODE: {settings['mode']} ({['Only IDs','IDs+Pages','Only Pages'][int(settings['mode'])-1]})
AVAILABLE ACTORS: {total_actors} (IDs + Pages)
AUTO-CALCULATED:
  • Base per actor: {base_limit} comments
  • Extra distribution: {remainder} actors will get +1
EMOJI: {'Yes' if settings['use_emoji'] else 'No'}
POST ID: {settings['post_id']}"""
    
    print_box(config_text, colors.BPINK)
    print_info(f"Active accounts/pages: {total_actors}")
    print()
    
    # Prepare tasks with auto-calculated distribution
    all_tasks = []
    
    # Distribute comments evenly
    for i, actor in enumerate(actor_details):
        # Each actor gets base_limit
        actor_comment_count = base_limit
        
        # First 'remainder' actors get 1 extra comment
        if i < remainder:
            actor_comment_count += 1
        
        # Create tasks for this actor
        for j in range(actor_comment_count):
            if user_data['success_count'] >= settings['target_total'] or not user_data['is_running']:
                break
            
            all_tasks.append({
                'cookie': actor['cookie'],
                'actor_id': actor['actor_id'],
                'post_id': settings['post_id'],
                'text': settings['comment_text'],
                'data': actor['data'].copy(),
                'doc_id': '7391620150945935',
                'name': actor['name'],
                'use_emoji': settings['use_emoji'],
                'type': actor['type']
            })
    
    # Shuffle for randomness
    random.shuffle(all_tasks)
    total_tasks = len(all_tasks)
    
    print_info(f"Total tasks prepared: {total_tasks}")
    print_info(f"Starting with 10 parallel threads...")
    print()
    
    # Run with ThreadPoolExecutor
    max_workers = min(70, total_tasks)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {}
        for task in all_tasks:
            if user_data['success_count'] >= settings['target_total'] or not user_data['is_running']:
                break
                
            future = executor.submit(
                submit_comment,
                task['cookie'],
                task['actor_id'],
                task['post_id'],
                task['text'],
                task['data'],
                task['doc_id'],
                task['name'],
                task['use_emoji'],
                task['type'] == 'page'  # is_page parameter
            )
            future_to_task[future] = task
        
        for future in as_completed(future_to_task):
            if not user_data['is_running']:
                break
                
            task = future_to_task[future]
            try:
                success, msg, name, aid, is_page = future.result(timeout=20)
                
                elapsed = time.time() - user_data['round_start_time']
                speed = calculate_speed(user_data['success_count'], elapsed)
                
                if success:
                    user_data['success_count'] += 1
                    status_icon = f"{colors.BGREEN}✓{colors.RESET}"
                    status_color = colors.GREEN
                else:
                    user_data['fail_count'] += 1
                    status_icon = f"{colors.BRED}✗{colors.RESET}"
                    status_color = colors.RED
                    if "block" in msg.lower():
                        user_data['blocked_cookies'].add(task['cookie'])
                
                # Original tags: P for Page, A for Account
                account_type = f"{colors.BPINK}[P]{colors.RESET}" if is_page else f"{colors.BCYAN}[A]{colors.RESET}"
                
                # Live update with speed
                print(f"  {status_icon} {account_type} {colors.BWHITE}{name[:20]:20}{colors.RESET} : {status_color}{msg:10}{colors.RESET} | {colors.BPINK}{user_data['success_count']}/{settings['target_total']}{colors.RESET} | {colors.LIGHT_PINK}{speed:.1f}/min{colors.RESET}")
                
                if user_data['success_count'] >= settings['target_total']:
                    break
                    
            except Exception as e:
                user_data['fail_count'] += 1
                print_error(f"Task error: {str(e)[:30]}")
    
    # Calculate final stats
    round_time = time.time() - user_data['round_start_time']
    final_speed = calculate_speed(user_data['success_count'], round_time)
    user_data['speed_history'].append(final_speed)
    
    # Show final results in a beautiful box
    result_text = f"""ROUND {user_data['current_round']} COMPLETE

✓ SUCCESS: {user_data['success_count']}
✗ FAILED: {user_data['fail_count']}
⛔ BLOCKED: {len(user_data['blocked_cookies'])}
🎯 TARGET: {settings['target_total']}

⚡ SPEED: {final_speed:.1f} comments/minute
⏱️ TIME: {format_time(round_time)}
📊 DISTRIBUTION: {base_limit} per actor + {remainder} extra
📊 ACCURACY: {(user_data['success_count']/(user_data['success_count']+user_data['fail_count'])*100) if (user_data['success_count']+user_data['fail_count'])>0 else 0:.1f}%"""
    
    print()
    print_box(result_text, colors.PINK)
    
    user_data['is_running'] = False
    user_data['current_round'] += 1
    
    return True

def show_statistics():
    """Show comprehensive statistics"""
    print_header("📊 COMPREHENSIVE STATISTICS", colors.BPINK)
    
    total_time = time.time() - user_data.get('start_time', time.time()) if user_data.get('start_time') else 0
    total_comments = user_data.get('success_count', 0) + user_data.get('fail_count', 0)
    avg_speed = sum(user_data.get('speed_history', [])) / len(user_data.get('speed_history', [1])) if user_data.get('speed_history') else 0
    
    stats_text = f"""SESSION OVERVIEW
✓ Total Success: {user_data.get('success_count', 0)}
✗ Total Failed: {user_data.get('fail_count', 0)}
⛔ Blocked Cookies: {len(user_data.get('blocked_cookies', set()))}
📊 Total Comments: {total_comments}

COOKIE STATISTICS
📁 Total Cookies: {len(user_data.get('cookies', []))}
✓ Valid Cookies: {sum(1 for d in user_data['cookie_data'].values() if d.get('valid', False))}
📄 Total Pages: {sum(len(d.get('pages', [])) for d in user_data['cookie_data'].values() if d.get('valid', False))}

PERFORMANCE
⚡ Average Speed: {avg_speed:.1f} comments/min
⏱️ Session Time: {format_time(total_time)}
🎯 Current Round: {user_data.get('current_round', 1)}"""
    
    print_box(stats_text, colors.PINK)
    
    if user_data.get('speed_history'):
        print()
        print_info("Round History:")
        for i, speed in enumerate(user_data['speed_history'], 1):
            bar = f"{colors.BG_PINK}{'█' * int(speed)}{colors.RESET}" if speed > 0 else ""
            print(f"  Round {i}: {colors.BPINK}{speed:.1f}/min{colors.RESET} {bar}")

def ask_next_round():
    """Ask user if they want next round"""
    print_header("🔄 NEXT ROUND OPTIONS", colors.BPINK)
    print(f"  {colors.BGREEN}[1]{colors.RESET} {colors.BWHITE}Yes - Same Settings{colors.RESET}")
    print(f"  {colors.BGREEN}[2]{colors.RESET} {colors.BWHITE}Yes - New Settings{colors.RESET}")
    print(f"  {colors.BGREEN}[3]{colors.RESET} {colors.BWHITE}Show Statistics{colors.RESET}")
    print(f"  {colors.BGREEN}[4]{colors.RESET} {colors.BWHITE}Clear Screen{colors.RESET}")
    print(f"  {colors.BRED}[0]{colors.RESET} {colors.BWHITE}No - Exit{colors.RESET}")
    print()
    
    choice = input(f"  {colors.BPINK}➤{colors.RESET} ").strip()
    return choice

def install_wmi_if_needed():
    """Check and install wmi if needed for Windows unique ID"""
    if platform.system() == "Windows":
        try:
            import wmi
        except ImportError:
            print_info("Installing wmi module for better device identification...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "wmi"])
                print_success("wmi installed successfully!")
            except:
                print_warning("Could not install wmi, using fallback device ID")

def main():
    """Main function"""
    global user_data
    
    # Windows specific setup
    if platform.system() == "Windows":
        install_wmi_if_needed()
    
    user_data['start_time'] = time.time()
    
    while True:
        clear_screen()
        print_banner()
        Privacy()
        
        # Step 1: Load cookies
        if not user_data['cookies']:
            print_header("📌 STEP 1: LOAD COOKIES", colors.BPINK)
            if not load_cookies_from_file():
                input(f"\n  {colors.BPINK}Press Enter to try again...{colors.RESET}")
                continue
        
        # Step 2: Pre-process if not done
        if not user_data['preprocessing_done']:
            preprocess_cookies()
            input(f"\n  {colors.BPINK}Press Enter to continue...{colors.RESET}")
            continue
        
        # Step 3: Get inputs for first round
        if not user_data.get('settings'):
            settings = get_user_inputs()
            if settings:
                user_data['settings'] = settings
                user_data['current_round'] = 1
                run_commenting(settings)
            else:
                input(f"\n  {colors.BPINK}Press Enter to try again...{colors.RESET}")
                continue
        
        # Step 4: Ask for next round
        while True:
            choice = ask_next_round()
            
            if choice == '1':  # Same settings
                if user_data.get('settings'):
                    run_commenting(user_data['settings'])
                else:
                    print_error("No settings found!")
                    
            elif choice == '2':  # New settings
                settings = get_user_inputs()
                if settings:
                    user_data['settings'] = settings
                    run_commenting(settings)
                    
            elif choice == '3':  # Show statistics
                show_statistics()
                input(f"\n  {colors.BPINK}Press Enter to continue...{colors.RESET}")
                
            elif choice == '4':  # Clear screen
                break
                
            elif choice == '0':  # Exit
                print_header("👋 GOODBYE!", colors.BPINK)
                print_info(f"Total Comments Posted: {user_data.get('success_count', 0)}")
                print_info(f"Session Time: {format_time(time.time() - user_data['start_time'])}")
                print()
                print_box("Thanks for using Facebook Auto Comment Tool! By Aftab", colors.PINK)
                sys.exit(0)
                
            else:
                print_error("Invalid choice!")
                time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {colors.BPINK}Exiting... Goodbye!{colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {colors.BRED}ERROR: {e}{colors.RESET}")
        sys.exit(1)