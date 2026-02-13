#!/usr/bin/env python3
"""
Web Shell Scanner with Telegram Notification
---------------------------------------------
Script untuk mendeteksi potensi web shell dengan notifikasi Telegram.
HANYA gunakan pada website yang Anda miliki atau memiliki izin!

Author: Security Scanner
Version: 2.0 (with Telegram Alert)
"""

import requests
import re
import sys
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Set
import argparse
from datetime import datetime
import json

class TelegramNotifier:
    """Class untuk mengirim notifikasi ke Telegram"""
    
    def __init__(self, bot_token: str, chat_id: str, enabled: bool = True):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = enabled
        self.api_url = f"https://api.telegram.org/bot{bot_token}"
        
    def send_message(self, message: str, parse_mode: str = "HTML") -> bool:
        """Kirim pesan ke Telegram"""
        if not self.enabled:
            return False
            
        try:
            url = f"{self.api_url}/sendMessage"
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }
            
            response = requests.post(url, json=payload, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"[!] Failed to send Telegram notification: {str(e)}")
            return False
    
    def send_start_notification(self, base_url: str, total_urls: int):
        """Kirim notifikasi awal scanning"""
        message = f"""
🔍 <b>Web Shell Scan Started</b>

<b>Target:</b> {base_url}
<b>URLs to Scan:</b> {total_urls}
<b>Started:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

⏳ Scanning in progress...
"""
        self.send_message(message.strip())
    
    def send_detection_alert(self, shell_info: Dict):
        """Kirim alert saat menemukan web shell"""
        reasons = "\n".join([f"  • {r}" for r in shell_info['reasons']])
        
        message = f"""
🚨 <b>SUSPICIOUS FILE DETECTED!</b>

<b>URL:</b> <code>{shell_info['url']}</code>

<b>Status Code:</b> {shell_info['status_code']}
<b>Content Length:</b> {shell_info['content_length']} bytes

<b>Reasons:</b>
{reasons}

<b>Time:</b> {datetime.now().strftime('%H:%M:%S')}

⚠️ <b>Action Required!</b>
"""
        self.send_message(message.strip())
    
    def send_summary_report(self, total_checked: int, found_shells: List[Dict], 
                           scan_duration: str, base_url: str):
        """Kirim laporan akhir scanning"""
        
        if found_shells:
            shells_list = "\n\n".join([
                f"{idx}. <code>{shell['url']}</code>\n   └ Size: {shell['content_length']} bytes"
                for idx, shell in enumerate(found_shells, 1)
            ])
            
            status_icon = "🚨"
            status_text = f"Found {len(found_shells)} suspicious file(s)"
        else:
            shells_list = "✅ No suspicious files detected in common locations."
            status_icon = "✅"
            status_text = "Scan Completed - Clean"
        
        message = f"""
{status_icon} <b>Scan Report - {status_text}</b>

<b>Target:</b> {base_url}
<b>Duration:</b> {scan_duration}
<b>URLs Checked:</b> {total_checked}
<b>Suspicious Files:</b> {len(found_shells)}

<b>Details:</b>
{shells_list}

<b>Completed:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        self.send_message(message.strip())


class WebShellScanner:
    def __init__(self, base_url: str, timeout: int = 10, threads: int = 10,
                 telegram_notifier: TelegramNotifier = None):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.threads = threads
        self.found_shells = []
        self.checked_urls = set()
        self.telegram = telegram_notifier
        self.start_time = None
        
        # Daftar nama file web shell yang umum
        self.common_webshell_names = [
            'c99.php', 'r57.php', 'shell.php', 'cmd.php', 'backdoor.php',
            'b374k.php', 'wso.php', 'bypass.php', 'alfa.php', 'WSO.php',
            'adminer.php', 'phpmyadmin.php', 'filemanager.php', 'uploader.php',
            'c100.php', 'r57shell.php', 'webshell.php', 'hack.php', 'x.php',
            'spy.php', 'mysql.php', 'madspot.php', 'mini.php', 'idx.php',
            'shell.aspx', 'cmd.aspx', 'webshell.aspx', 'asp.aspx',
            'shell.jsp', 'cmd.jsp', 'webshell.jsp', 'jspspy.jsp',
            'shell.py', 'webshell.py', 'backdoor.py'
        ]
        
        # Ekstensi file mencurigakan
        self.suspicious_extensions = [
            '.php', '.php3', '.php4', '.php5', '.phtml', '.phar',
            '.aspx', '.asp', '.cer', '.asa',
            '.jsp', '.jspx',
            '.py', '.pl', '.cgi',
            '.sh', '.bash'
        ]
        
        # Direktori umum tempat web shell sering diupload
        self.common_directories = [
            '/uploads/', '/upload/', '/files/', '/file/', '/images/', '/image/',
            '/media/', '/assets/', '/temp/', '/tmp/', '/cache/', '/backup/',
            '/admin/', '/administrator/', '/wp-content/uploads/', '/wp-content/themes/',
            '/wp-includes/', '/includes/', '/inc/', '/modules/', '/plugins/',
            '/components/', '/content/', '/data/', '/public/', '/storage/'
        ]
        
        # Pattern code berbahaya dalam response
        self.malicious_patterns = [
            r'eval\s*\(\s*base64_decode',
            r'eval\s*\(\s*gzinflate',
            r'eval\s*\(\s*str_rot13',
            r'assert\s*\(\s*base64_decode',
            r'system\s*\(',
            r'exec\s*\(',
            r'passthru\s*\(',
            r'shell_exec\s*\(',
            r'base64_decode\s*\(\s*[\'"][\w+/=]{50,}',
            r'FilesMan',
            r'c99shell',
            r'r57shell',
            r'WSO\s*Shell',
            r'b374k',
            r'Backdoor',
            r'phpspy',
            r'SafeMode',
            r'uname\s*-a',
            r'chmod\s+777',
            r'preg_replace.*\/e',
            r'\\$_(GET|POST|REQUEST)\[.*\]\s*\(',
        ]
        
        # Headers untuk request
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Security Scanner Bot) WebShell Detector/2.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

    def check_url(self, url: str) -> Dict:
        """Cek URL untuk potensi web shell"""
        if url in self.checked_urls:
            return None
            
        self.checked_urls.add(url)
        
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout, 
                                   allow_redirects=False, verify=False)
            
            result = {
                'url': url,
                'status_code': response.status_code,
                'suspicious': False,
                'reasons': [],
                'content_length': len(response.content)
            }
            
            # Cek status code
            if response.status_code == 200:
                content = response.text
                
                # Cek pattern berbahaya dalam content
                for pattern in self.malicious_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        result['suspicious'] = True
                        result['reasons'].append(f"Malicious pattern: {pattern[:50]}")
                
                # Cek header mencurigakan
                if 'text/html' not in response.headers.get('Content-Type', ''):
                    if any(ext in url.lower() for ext in ['.php', '.aspx', '.jsp']):
                        result['suspicious'] = True
                        result['reasons'].append("Suspicious content-type for script file")
                
                # Cek ukuran file (web shell biasanya 10KB - 500KB)
                if 10000 < len(response.content) < 500000:
                    # Cek ratio code vs text
                    code_indicators = len(re.findall(r'[\{\}\(\)\$\;]', content))
                    if code_indicators > len(content) * 0.1:
                        result['suspicious'] = True
                        result['reasons'].append("High code-to-text ratio")
                
                return result
                
        except requests.exceptions.RequestException as e:
            return None
        
        return None

    def scan_common_paths(self) -> List[str]:
        """Generate daftar URL untuk di-scan"""
        urls_to_scan = []
        
        # Scan nama file web shell umum di root dan direktori umum
        for shell_name in self.common_webshell_names:
            # Di root
            urls_to_scan.append(urljoin(self.base_url, shell_name))
            
            # Di direktori umum
            for directory in self.common_directories:
                urls_to_scan.append(urljoin(self.base_url, directory + shell_name))
        
        return urls_to_scan

    def scan(self):
        """Mulai scanning"""
        self.start_time = datetime.now()
        
        print(f"\n{'='*70}")
        print(f"Web Shell Scanner with Telegram Notification")
        print(f"{'='*70}")
        print(f"Target: {self.base_url}")
        print(f"Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Telegram: {'Enabled ✓' if self.telegram and self.telegram.enabled else 'Disabled'}")
        print(f"{'='*70}\n")
        
        urls_to_scan = self.scan_common_paths()
        total_urls = len(urls_to_scan)
        
        print(f"[*] Total URLs to scan: {total_urls}")
        print(f"[*] Using {self.threads} threads\n")
        
        # Kirim notifikasi start
        if self.telegram:
            self.telegram.send_start_notification(self.base_url, total_urls)
        
        # Scan dengan threading
        completed = 0
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            future_to_url = {executor.submit(self.check_url, url): url 
                           for url in urls_to_scan}
            
            for future in as_completed(future_to_url):
                completed += 1
                if completed % 50 == 0:
                    print(f"[*] Progress: {completed}/{total_urls} URLs scanned...")
                
                result = future.result()
                if result and result['suspicious']:
                    self.found_shells.append(result)
                    print(f"\n[!] SUSPICIOUS FILE FOUND: {result['url']}")
                    print(f"    Status: {result['status_code']}")
                    print(f"    Reasons: {', '.join(result['reasons'])}")
                    
                    # Kirim alert ke Telegram
                    if self.telegram:
                        self.telegram.send_detection_alert(result)
        
        # Hitung durasi
        end_time = datetime.now()
        duration = end_time - self.start_time
        duration_str = str(duration).split('.')[0]  # Format: HH:MM:SS
        
        # Tampilkan hasil
        self.print_results()
        
        # Kirim summary report ke Telegram
        if self.telegram:
            self.telegram.send_summary_report(
                len(self.checked_urls),
                self.found_shells,
                duration_str,
                self.base_url
            )

    def print_results(self):
        """Cetak hasil scanning"""
        print(f"\n{'='*70}")
        print(f"SCAN RESULTS")
        print(f"{'='*70}\n")
        
        if self.found_shells:
            print(f"[!] Found {len(self.found_shells)} suspicious files:\n")
            
            for idx, shell in enumerate(self.found_shells, 1):
                print(f"{idx}. {shell['url']}")
                print(f"   Status Code: {shell['status_code']}")
                print(f"   Content Length: {shell['content_length']} bytes")
                print(f"   Reasons:")
                for reason in shell['reasons']:
                    print(f"     - {reason}")
                print()
        else:
            print("[+] No suspicious files detected in common locations.")
            print("[+] This doesn't guarantee the site is clean.")
            print("[+] Consider deeper scanning and manual inspection.\n")
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        print(f"{'='*70}")
        print(f"Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration: {str(duration).split('.')[0]}")
        print(f"Total URLs checked: {len(self.checked_urls)}")
        print(f"{'='*70}\n")


def test_telegram_connection(bot_token: str, chat_id: str) -> bool:
    """Test koneksi ke Telegram"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": "🔔 <b>Telegram Connection Test</b>\n\nYour Web Shell Scanner is successfully connected to Telegram!\n\n✅ Notifications are enabled.",
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, json=payload, timeout=10)
        
        if response.status_code == 200:
            print("[✓] Telegram connection test: SUCCESS")
            return True
        else:
            print(f"[✗] Telegram connection test: FAILED")
            print(f"    Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"[✗] Telegram connection test: ERROR")
        print(f"    Error: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Web Shell Scanner with Telegram Notification',
        epilog='Example: python webshell_scanner_telegram.py -u https://example.com -tb YOUR_BOT_TOKEN -tc YOUR_CHAT_ID',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-u', '--url', required=True, 
                       help='Target website URL (e.g., https://example.com)')
    parser.add_argument('-t', '--timeout', type=int, default=10,
                       help='Request timeout in seconds (default: 10)')
    parser.add_argument('-w', '--workers', type=int, default=10,
                       help='Number of worker threads (default: 10)')
    
    # Telegram options
    telegram_group = parser.add_argument_group('Telegram Notification Options')
    telegram_group.add_argument('-tb', '--telegram-bot-token', 
                               help='Telegram Bot Token (dari @BotFather)')
    telegram_group.add_argument('-tc', '--telegram-chat-id',
                               help='Telegram Chat ID (user atau grup)')
    telegram_group.add_argument('--test-telegram', action='store_true',
                               help='Test koneksi Telegram dan keluar')
    telegram_group.add_argument('--no-telegram', action='store_true',
                               help='Disable notifikasi Telegram')
    
    args = parser.parse_args()
    
    # Test Telegram connection jika diminta
    if args.test_telegram:
        if not args.telegram_bot_token or not args.telegram_chat_id:
            print("[ERROR] Bot token dan chat ID diperlukan untuk test")
            print("Usage: python script.py --test-telegram -tb BOT_TOKEN -tc CHAT_ID")
            sys.exit(1)
        
        test_telegram_connection(args.telegram_bot_token, args.telegram_chat_id)
        sys.exit(0)
    
    # Validasi URL
    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print("[ERROR] Invalid URL format. Please use format: https://example.com")
        sys.exit(1)
    
    # Setup Telegram notifier
    telegram_notifier = None
    if not args.no_telegram:
        if args.telegram_bot_token and args.telegram_chat_id:
            telegram_notifier = TelegramNotifier(
                args.telegram_bot_token, 
                args.telegram_chat_id,
                enabled=True
            )
            print("[*] Telegram notifications: ENABLED")
        else:
            print("[!] Telegram credentials not provided. Notifications: DISABLED")
            print("    Use -tb and -tc to enable Telegram notifications")
    
    # Disclaimer
    print("\n" + "="*70)
    print("WARNING - LEGAL DISCLAIMER")
    print("="*70)
    print("This tool should ONLY be used on websites you own or have")
    print("explicit written permission to test. Unauthorized scanning")
    print("may be ILLEGAL and could result in criminal prosecution.")
    print("="*70)
    
    response = input("\nDo you have permission to scan this website? (yes/no): ")
    if response.lower() != 'yes':
        print("\n[!] Scan cancelled. Obtain proper authorization before scanning.")
        sys.exit(0)
    
    # Mulai scanning
    try:
        scanner = WebShellScanner(
            args.url, 
            timeout=args.timeout, 
            threads=args.workers,
            telegram_notifier=telegram_notifier
        )
        scanner.scan()
    except KeyboardInterrupt:
        print("\n\n[!] Scan interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
