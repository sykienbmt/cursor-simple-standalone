#!/usr/bin/env python3
"""
Cursor Simple - Lightweight Cross-Platform Tool
Version: 1.3.0
Author: Cursor Free VIP Community
License: Educational Use Only

Features:
  1. Quit Cursor
  2. Reset Machine ID
  3. Update Token (Auto-fetch from API)
  4. Quick Reset (Machine ID + Token)
  5. Get Account Info (View account details)

Supported Platforms: Windows | macOS | Linux
Dependencies: colorama (optional), requests (for API integration)
"""

import os
import sys
import sqlite3
import json
import uuid
import platform
import subprocess
import time
from pathlib import Path

# Try to import requests for API calls
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Try to import colorama, fallback to no colors if not available
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    HAS_COLOR = True
except ImportError:
    # Fallback: No colors
    class Fore:
        CYAN = GREEN = YELLOW = RED = WHITE = ''
    class Style:
        RESET_ALL = ''
    HAS_COLOR = False

# Emoji constants
EMOJI = {
    'MENU': '📋',
    'QUIT': '❌',
    'RESET': '🔄',
    'TOKEN': '🔑',
    'SUCCESS': '✅',
    'ERROR': '❌',
    'INFO': 'ℹ️',
    'WARNING': '⚠️',
    'ARROW': '➜',
    'ACCOUNT': '👤'
}

class CursorSimple:
    def __init__(self):
        self.system = platform.system()
        self.paths = self._get_cursor_paths()
        
    def _get_cursor_paths(self):
        """Get Cursor paths based on OS"""
        if self.system == "Windows":
            appdata = os.getenv("APPDATA")
            localappdata = os.getenv("LOCALAPPDATA")
            return {
                'sqlite': os.path.join(appdata, "Cursor", "User", "globalStorage", "state.vscdb"),
                'storage': os.path.join(appdata, "Cursor", "User", "globalStorage", "storage.json"),
                'machine_id': os.path.join(appdata, "Cursor", "machineId"),
                'process_name': 'Cursor.exe'
            }
        elif self.system == "Darwin":  # macOS
            return {
                'sqlite': os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/state.vscdb"),
                'storage': os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/storage.json"),
                'machine_id': os.path.expanduser("~/Library/Application Support/Cursor/machineId"),
                'process_name': 'Cursor'
            }
        else:  # Linux
            # Try both .config/Cursor and .config/cursor
            config_base = os.path.expanduser("~/.config")
            cursor_dir = None
            
            for dirname in ['Cursor', 'cursor']:
                test_path = os.path.join(config_base, dirname)
                if os.path.exists(test_path):
                    cursor_dir = test_path
                    break
            
            if not cursor_dir:
                cursor_dir = os.path.join(config_base, "Cursor")
            
            return {
                'sqlite': os.path.join(cursor_dir, "User/globalStorage/state.vscdb"),
                'storage': os.path.join(cursor_dir, "User/globalStorage/storage.json"),
                'machine_id': os.path.join(cursor_dir, "machineid"),
                'process_name': 'cursor'
            }
    
    def quit_cursor(self):
        """Quit/Kill Cursor process"""
        print(f"\n{Fore.CYAN}{EMOJI['QUIT']} Quitting Cursor...{Style.RESET_ALL}")
        
        try:
            if self.system == "Windows":
                # Kill Cursor process on Windows
                subprocess.run(['taskkill', '/F', '/IM', 'Cursor.exe'], 
                             stderr=subprocess.DEVNULL, 
                             stdout=subprocess.DEVNULL)
            else:
                # Kill Cursor process on macOS/Linux
                subprocess.run(['pkill', '-9', self.paths['process_name']], 
                             stderr=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL)
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Cursor process terminated{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} Could not kill Cursor process: {str(e)}{Style.RESET_ALL}")
            return False
    
    def _generate_machine_ids(self):
        """Generate all required machine IDs"""
        import secrets
        
        return {
            'devDeviceId': str(uuid.uuid4()),
            'machineId': secrets.token_hex(32),
            'macMachineId': secrets.token_hex(64),
            'sqmId': "{" + str(uuid.uuid4()).upper() + "}"
        }
    
    def _update_windows_registry(self, new_guid):
        """Update Windows Registry MachineGuid (Windows only)"""
        if self.system != "Windows":
            return False
        
        try:
            import winreg
            registry_path = r"SOFTWARE\Microsoft\Cryptography"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
            
            try:
                old_guid = winreg.QueryValueEx(key, "MachineGuid")[0]
                winreg.SetValueEx(key, "MachineGuid.backup", 0, winreg.REG_SZ, old_guid)
            except:
                pass
            
            winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_guid)
            winreg.CloseKey(key)
            return True
            
        except Exception as e:
            return False
    
    def reset_machine_id(self):
        """Reset Cursor Machine ID"""
        print(f"\n{Fore.CYAN}{EMOJI['RESET']} Resetting Machine ID...{Style.RESET_ALL}")
        
        try:
            # Generate all required IDs
            ids = self._generate_machine_ids()
            
            # Update machineId file
            machine_id_path = self.paths['machine_id']
            os.makedirs(os.path.dirname(machine_id_path), exist_ok=True)
            
            with open(machine_id_path, 'w') as f:
                f.write(ids['devDeviceId'])
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Machine ID file updated{Style.RESET_ALL}")
            
            # Update storage.json
            storage_path = self.paths['storage']
            if os.path.exists(storage_path):
                try:
                    with open(storage_path, 'r') as f:
                        storage_data = json.load(f)
                except:
                    storage_data = {}
            else:
                storage_data = {}
                os.makedirs(os.path.dirname(storage_path), exist_ok=True)
            
            storage_data['telemetry.devDeviceId'] = ids['devDeviceId']
            storage_data['telemetry.machineId'] = ids['machineId']
            storage_data['telemetry.macMachineId'] = ids['macMachineId']
            storage_data['telemetry.sqmId'] = ids['sqmId']
            storage_data['storage.serviceMachineId'] = ids['devDeviceId']
            
            with open(storage_path, 'w') as f:
                json.dump(storage_data, f, indent=2)
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Storage.json updated{Style.RESET_ALL}")
            
            # Update SQLite database
            sqlite_path = self.paths['sqlite']
            if os.path.exists(sqlite_path):
                try:
                    conn = sqlite3.connect(sqlite_path)
                    cursor = conn.cursor()
                    
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS ItemTable (
                            key TEXT PRIMARY KEY,
                            value TEXT
                        )
                    ''')
                    
                    updates = [
                        ('telemetry.devDeviceId', ids['devDeviceId']),
                        ('telemetry.machineId', ids['machineId']),
                        ('telemetry.macMachineId', ids['macMachineId']),
                        ('telemetry.sqmId', ids['sqmId']),
                        ('storage.serviceMachineId', ids['devDeviceId'])
                    ]
                    
                    for key, value in updates:
                        cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
                    
                    conn.commit()
                    conn.close()
                    
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} SQLite database updated{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.YELLOW}{EMOJI['WARNING']} Could not update SQLite: {str(e)}{Style.RESET_ALL}")
            
            # Update Windows Registry (Windows only)
            if self.system == "Windows":
                new_registry_guid = str(uuid.uuid4())
                if self._update_windows_registry(new_registry_guid):
                    print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Windows Registry updated{Style.RESET_ALL}")
            
            print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} Machine ID reset successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}New Machine ID: {ids['devDeviceId']}{Style.RESET_ALL}")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to reset Machine ID: {str(e)}{Style.RESET_ALL}")
            return False
    
    def refresh_cursor_token(self, token):
        """Refresh token via Cursor API server to get valid accessToken
        
        This is CRITICAL! The token from cookie/API must be refreshed
        through Cursor's token server to get a valid accessToken.
        """
        if not HAS_REQUESTS:
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} Cannot refresh token - 'requests' not installed{Style.RESET_ALL}")
            return token
        
        try:
            # Ensure token is properly URL encoded
            if '%3A%3A' not in token and '::' in token:
                token = token.replace('::', '%3A%3A')
            
            # Cursor token refresh server
            refresh_server = 'https://token.cursorpro.com.cn'
            url = f"{refresh_server}/reftoken?token={token}"
            
            print(f"{Fore.CYAN}{EMOJI['INFO']} Refreshing token via Cursor server...{Style.RESET_ALL}")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == 0 and data.get('msg') == "获取成功":
                    access_token = data.get('data', {}).get('accessToken')
                    days_left = data.get('data', {}).get('days_left', 0)
                    expire_time = data.get('data', {}).get('expire_time', 'Unknown')
                    
                    if access_token:
                        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Token refreshed successfully!{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}├─ Valid for: {days_left} days{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}└─ Expires: {expire_time}{Style.RESET_ALL}\n")
                        return access_token
                    else:
                        print(f"{Fore.YELLOW}{EMOJI['WARNING']} No accessToken in response, using original{Style.RESET_ALL}")
                else:
                    error_msg = data.get('msg', 'Unknown error')
                    print(f"{Fore.YELLOW}{EMOJI['WARNING']} Refresh failed: {error_msg}, using original token{Style.RESET_ALL}")
            else:
                print(f"{Fore.YELLOW}{EMOJI['WARNING']} Server error (HTTP {response.status_code}), using original token{Style.RESET_ALL}")
        
        except requests.Timeout:
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} Refresh timeout, using original token{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.YELLOW}{EMOJI['WARNING']} Refresh error: {str(e)}, using original token{Style.RESET_ALL}")
        
        # Fallback: extract JWT from original token if refresh fails
        if '%3A%3A' in token:
            return token.split('%3A%3A')[-1]
        elif '::' in token:
            return token.split('::')[-1]
        else:
            return token
    
    def fetch_token_from_api(self, api_url, max_retries=3):
        """Fetch token from Google Apps Script API with retry logic"""
        if not HAS_REQUESTS:
            print(f"{Fore.RED}{EMOJI['ERROR']} 'requests' module not installed{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Install it with: pip install requests{Style.RESET_ALL}")
            return None
        
        for attempt in range(1, max_retries + 1):
            try:
                if attempt > 1:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} Retry {attempt}/{max_retries}...{Style.RESET_ALL}")
                else:
                    print(f"{Fore.CYAN}{EMOJI['INFO']} Fetching token from API...{Style.RESET_ALL}")
                
                # Increased timeout to 60 seconds for Google Apps Script
                response = requests.get(api_url, timeout=60)
                response.raise_for_status()
                
                data = response.json()
                
                if not data.get('success'):
                    error_msg = data.get('error', 'Unknown error')
                    print(f"{Fore.RED}{EMOJI['ERROR']} API Error: {error_msg}{Style.RESET_ALL}")
                    if attempt < max_retries:
                        print(f"{Fore.YELLOW}{EMOJI['INFO']} Waiting 3 seconds before retry...{Style.RESET_ALL}")
                        time.sleep(3)
                        continue
                    return None
                
                token_data = data.get('data', {})
                token = token_data.get('token', '')
                account = token_data.get('account', '')
                row = data.get('row', 'N/A')
                
                if not token:
                    print(f"{Fore.RED}{EMOJI['ERROR']} No token found in API response{Style.RESET_ALL}")
                    if attempt < max_retries:
                        print(f"{Fore.YELLOW}{EMOJI['INFO']} Waiting 3 seconds before retry...{Style.RESET_ALL}")
                        time.sleep(3)
                        continue
                    return None
                
                # Parse account info (format: email/password)
                email = 'user@cursor.sh'
                password = ''
                
                if account and '/' in account:
                    parts = account.split('/', 1)
                    email = parts[0]
                    password = parts[1] if len(parts) > 1 else ''
                
                print(f"\n{Fore.GREEN}{EMOJI['SUCCESS']} Token fetched successfully!{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Row: {row}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Email: {email}{Style.RESET_ALL}")
                if password:
                    print(f"{Fore.CYAN}Password: {password}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}Token (first 50 chars): {token[:50]}...{Style.RESET_ALL}")
                print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
                
                return {
                    'token': token,
                    'email': email,
                    'password': password,
                    'row': row
                }
                
            except requests.Timeout:
                print(f"{Fore.RED}{EMOJI['ERROR']} Request timeout (60s){Style.RESET_ALL}")
                if attempt < max_retries:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} Waiting 5 seconds before retry...{Style.RESET_ALL}")
                    time.sleep(5)
                    continue
            except requests.RequestException as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} Request failed: {str(e)}{Style.RESET_ALL}")
                if attempt < max_retries:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} Waiting 3 seconds before retry...{Style.RESET_ALL}")
                    time.sleep(3)
                    continue
            except json.JSONDecodeError:
                print(f"{Fore.RED}{EMOJI['ERROR']} Invalid JSON response{Style.RESET_ALL}")
                if attempt < max_retries:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} Waiting 3 seconds before retry...{Style.RESET_ALL}")
                    time.sleep(3)
                    continue
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} Unexpected error: {str(e)}{Style.RESET_ALL}")
                if attempt < max_retries:
                    print(f"{Fore.YELLOW}{EMOJI['INFO']} Waiting 3 seconds before retry...{Style.RESET_ALL}")
                    time.sleep(3)
                    continue
        
        # All retries failed
        print(f"{Fore.RED}{EMOJI['ERROR']} Failed to fetch token after {max_retries} attempts{Style.RESET_ALL}")
        return None
    
    def get_account_info(self):
        """Get and display account information from API"""
        print(f"\n{Fore.CYAN}{EMOJI['ACCOUNT']} Get Account Information{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        if not HAS_REQUESTS:
            print(f"{Fore.RED}{EMOJI['ERROR']} 'requests' module not installed{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Install it with: pip install requests{Style.RESET_ALL}")
            return False
        
        print(f"{Fore.CYAN}{EMOJI['INFO']} Fetching account from API...{Style.RESET_ALL}\n")
        
        # Use the default API
        api_url = "https://script.google.com/macros/s/AKfycbxN6lLVmJk8b8qgi63eXeaeBzaiD0xeZnXlv6_PfbGBrZr3BhN7LT0QyMMga-ixT7M_/exec"
        
        token_data = self.fetch_token_from_api(api_url)
        
        if not token_data:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to fetch account information{Style.RESET_ALL}")
            return False
        
        # Extract information
        token_full = token_data['token']
        email = token_data['email']
        password = token_data.get('password', 'N/A')
        row = token_data.get('row', 'N/A')
        
        # Refresh token to get the actual accessToken
        print(f"{Fore.CYAN}{EMOJI['INFO']} Refreshing token...{Style.RESET_ALL}")
        access_token = self.refresh_cursor_token(token_full)
        
        # Display full account information
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{EMOJI['ACCOUNT']} Account Information{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}Row Number:{Style.RESET_ALL} {row}")
        print(f"{Fore.CYAN}{'─'*60}{Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}Username/Email:{Style.RESET_ALL}")
        print(f"  {email}")
        
        print(f"\n{Fore.YELLOW}Password:{Style.RESET_ALL}")
        print(f"  {password}")
        
        print(f"\n{Fore.YELLOW}Full Token (with prefix):{Style.RESET_ALL}")
        print(f"  {token_full}")
        
        print(f"\n{Fore.YELLOW}Access Token (refreshed):{Style.RESET_ALL}")
        print(f"  {access_token}")
        
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Account information displayed successfully!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
        
        return True
    
    def update_token(self):
        """Quick update token - auto-fetch from API, no confirmations"""
        print(f"\n{Fore.CYAN}{EMOJI['TOKEN']} Quick Update Token{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}{EMOJI['INFO']} Auto mode - fetching from API...{Style.RESET_ALL}\n")
        
        # Step 1: Close Cursor first (CRITICAL!)
        print(f"{Fore.CYAN}{EMOJI['INFO']} Step 1/3: Closing Cursor...{Style.RESET_ALL}")
        if not self.quit_cursor():
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to close Cursor{Style.RESET_ALL}")
            return False
        
        # Auto-fetch from API (no questions asked)
        print(f"\n{Fore.CYAN}{EMOJI['INFO']} Step 2/3: Fetching token...{Style.RESET_ALL}")
        api_url = "https://script.google.com/macros/s/AKfycbxN6lLVmJk8b8qgi63eXeaeBzaiD0xeZnXlv6_PfbGBrZr3BhN7LT0QyMMga-ixT7M_/exec"
        
        token_data = self.fetch_token_from_api(api_url)
        
        if not token_data:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to fetch token from API{Style.RESET_ALL}")
            return False
        
        # Get full token and email from API
        token_full = token_data['token']
        email = token_data['email']
        password = token_data.get('password', '')
        
        # Refresh token via Cursor server to get valid accessToken
        print(f"{Fore.CYAN}{EMOJI['INFO']} Token before refresh (first 50 chars): {token_full[:50]}...{Style.RESET_ALL}")
        token = self.refresh_cursor_token(token_full)
        print(f"{Fore.CYAN}{EMOJI['INFO']} Token after refresh (first 50 chars): {token[:50]}...{Style.RESET_ALL}")
        
        # Update SQLite database (no confirmation)
        print(f"\n{Fore.CYAN}{EMOJI['INFO']} Step 3/3: Updating database...{Style.RESET_ALL}")
        try:
            sqlite_path = self.paths['sqlite']
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)
            
            # Create database if it doesn't exist
            if not os.path.exists(sqlite_path):
                conn = sqlite3.connect(sqlite_path)
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ItemTable (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                ''')
                conn.commit()
                conn.close()
            
            # Update authentication data
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()
            
            # Set pragma for better performance
            cursor.execute("PRAGMA journal_mode = WAL")
            cursor.execute("PRAGMA synchronous = NORMAL")
            
            # Update all necessary authentication keys
            import time
            current_timestamp = int(time.time() * 1000)  # milliseconds
            
            updates = [
                # Core authentication tokens
                ('cursorAuth/accessToken', token),
                ('cursorAuth/refreshToken', token),
                
                # User information
                ('cursorAuth/cachedEmail', email),
                ('cursorAuth/cachedSignUpType', 'Auth_0'),
                
                # Token metadata
                ('cursorAuth/tokenType', 'bearer'),
                ('cursorAuth/expiresAt', str(current_timestamp + 86400000)),  # 24 hours from now
                
                # Session tokens (some Cursor versions check these)
                ('workos-session', token),
                ('WorkosCursorSessionToken', token),  # Cookie-based session
                
                # User profile (helps avoid re-authentication)
                ('cursorAuth/cachedName', email.split('@')[0]),  # Username from email
            ]
            
            for key, value in updates:
                cursor.execute("""
                    INSERT OR REPLACE INTO ItemTable (key, value) 
                    VALUES (?, ?)
                """, (key, value))
                print(f"{Fore.GREEN}  ✓ {key}{Style.RESET_ALL}")
            
            conn.commit()
            conn.close()
            
            # Verify the update by reading back
            print(f"\n{Fore.CYAN}{EMOJI['INFO']} Verifying database update...{Style.RESET_ALL}")
            conn = sqlite3.connect(sqlite_path)
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM ItemTable WHERE key = 'cursorAuth/accessToken'")
            saved_token = cursor.fetchone()
            if saved_token:
                print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Database verified - Token saved: {saved_token[0][:50]}...{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}{EMOJI['ERROR']} Warning: Could not verify token in database!{Style.RESET_ALL}")
            conn.close()
            
            # Display account info
            print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Token Updated Successfully!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Account Information:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}├─ Email: {email}{Style.RESET_ALL}")
            if password:
                print(f"{Fore.CYAN}├─ Password: {password}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}└─ Token: {token[:40]}...{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} You can now start Cursor and use the new account!{Style.RESET_ALL}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to update token: {str(e)}{Style.RESET_ALL}")
            return False
    
    def clear_screen(self):
        """Clear terminal screen"""
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')
    
    def quick_reset(self):
        """Quick reset: Machine ID + Token in one go (no confirmations)"""
        print(f"\n{Fore.CYAN}{EMOJI['RESET']} Quick Reset - Machine ID + Token{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}{EMOJI['INFO']} Auto mode - no confirmations required{Style.RESET_ALL}\n")
        
        # Step 1: Quit Cursor
        print(f"{Fore.CYAN}[1/3] Quitting Cursor...{Style.RESET_ALL}")
        self.quit_cursor()
        
        # Step 2: Reset Machine ID
        print(f"\n{Fore.CYAN}[2/3] Resetting Machine ID...{Style.RESET_ALL}")
        
        try:
            ids = self._generate_machine_ids()
            
            # Update machineId file
            machine_id_path = self.paths['machine_id']
            os.makedirs(os.path.dirname(machine_id_path), exist_ok=True)
            with open(machine_id_path, 'w') as f:
                f.write(ids['devDeviceId'])
            
            # Update storage.json
            storage_path = self.paths['storage']
            if os.path.exists(storage_path):
                with open(storage_path, 'r') as f:
                    storage_data = json.load(f)
            else:
                storage_data = {}
                os.makedirs(os.path.dirname(storage_path), exist_ok=True)
            
            storage_data['telemetry.devDeviceId'] = ids['devDeviceId']
            storage_data['telemetry.machineId'] = ids['machineId']
            storage_data['telemetry.macMachineId'] = ids['macMachineId']
            storage_data['telemetry.sqmId'] = ids['sqmId']
            storage_data['storage.serviceMachineId'] = ids['devDeviceId']
            
            with open(storage_path, 'w') as f:
                json.dump(storage_data, f, indent=2)
            
            # Update SQLite
            if os.path.exists(self.paths['sqlite']):
                conn = sqlite3.connect(self.paths['sqlite'])
                cursor = conn.cursor()
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS ItemTable (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                ''')
                
                updates = [
                    ('telemetry.devDeviceId', ids['devDeviceId']),
                    ('telemetry.machineId', ids['machineId']),
                    ('telemetry.macMachineId', ids['macMachineId']),
                    ('telemetry.sqmId', ids['sqmId']),
                    ('storage.serviceMachineId', ids['devDeviceId'])
                ]
                
                for key, value in updates:
                    cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
                
                conn.commit()
                conn.close()
            
            # Update Windows Registry (Windows only)
            if self.system == "Windows":
                new_registry_guid = str(uuid.uuid4())
                self._update_windows_registry(new_registry_guid)
            
            print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Machine ID reset: {ids['devDeviceId'][:16]}...{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Machine ID reset failed: {str(e)}{Style.RESET_ALL}")
            return False
        
        # Step 3: Fetch and update token
        print(f"\n{Fore.CYAN}[3/3] Fetching and updating token...{Style.RESET_ALL}")
        
        api_url = "https://script.google.com/macros/s/AKfycbxN6lLVmJk8b8qgi63eXeaeBzaiD0xeZnXlv6_PfbGBrZr3BhN7LT0QyMMga-ixT7M_/exec"
        
        token_data = self.fetch_token_from_api(api_url)
        if not token_data:
            print(f"{Fore.RED}{EMOJI['ERROR']} Failed to fetch token{Style.RESET_ALL}")
            return False
        
        # Refresh token
        token = self.refresh_cursor_token(token_data['token'])
        email = token_data['email']
        password = token_data.get('password', '')
        
        # Update database
        try:
            conn = sqlite3.connect(self.paths['sqlite'])
            cursor = conn.cursor()
            
            # Update all necessary authentication keys
            import time
            current_timestamp = int(time.time() * 1000)  # milliseconds
            
            updates = [
                # Core authentication tokens
                ('cursorAuth/accessToken', token),
                ('cursorAuth/refreshToken', token),
                
                # User information
                ('cursorAuth/cachedEmail', email),
                ('cursorAuth/cachedSignUpType', 'Auth_0'),
                
                # Token metadata
                ('cursorAuth/tokenType', 'bearer'),
                ('cursorAuth/expiresAt', str(current_timestamp + 86400000)),  # 24 hours from now
                
                # Session tokens (some Cursor versions check these)
                ('workos-session', token),
                ('WorkosCursorSessionToken', token),  # Cookie-based session
                
                # User profile (helps avoid re-authentication)
                ('cursorAuth/cachedName', email.split('@')[0]),  # Username from email
            ]
            
            for key, value in updates:
                cursor.execute("INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)", (key, value))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"{Fore.RED}{EMOJI['ERROR']} Token update failed: {str(e)}{Style.RESET_ALL}")
            return False
        
        # Display complete info
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} Quick Reset Complete!{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Account Information:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├─ Email: {email}{Style.RESET_ALL}")
        if password:
            print(f"{Fore.CYAN}├─ Password: {password}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└─ Token: {token[:40]}...{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{EMOJI['SUCCESS']} You can now start Cursor and use the new account!{Style.RESET_ALL}")
        
        return True
    
    def print_menu(self):
        """Print main menu"""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{EMOJI['MENU']} Cursor Simple - Cross-Platform Tool{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}1.{Style.RESET_ALL} {EMOJI['QUIT']} Quit Cursor")
        print(f"{Fore.GREEN}2.{Style.RESET_ALL} {EMOJI['RESET']} Reset Machine ID")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} {EMOJI['TOKEN']} Quick Update Token (Auto){Style.RESET_ALL}")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} {EMOJI['SUCCESS']} Quick Reset (Machine ID + Token){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}5.{Style.RESET_ALL} {EMOJI['ACCOUNT']} Get Account Info{Style.RESET_ALL}")
        print(f"{Fore.GREEN}0.{Style.RESET_ALL} {EMOJI['QUIT']} Exit")
        
        print(f"\n{Fore.CYAN}System: {self.system}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}SQLite Path: {self.paths['sqlite']}{Style.RESET_ALL}")
        
        if not HAS_COLOR:
            print(f"\nNote: Install 'colorama' for colored output: pip install colorama")
    
    def run(self):
        """Main program loop"""
        while True:
            self.print_menu()
            
            try:
                choice = input(f"\n{Fore.YELLOW}{EMOJI['ARROW']} Enter choice (0-5): {Style.RESET_ALL}").strip()
                
                if choice == '0':
                    print(f"\n{Fore.CYAN}{EMOJI['INFO']} Goodbye!{Style.RESET_ALL}")
                    break
                elif choice == '1':
                    self.quit_cursor()
                elif choice == '2':
                    self.quit_cursor()  # Quit first
                    self.reset_machine_id()
                elif choice == '3':
                    self.quit_cursor()  # Quit first
                    self.update_token()
                elif choice == '4':
                    self.quick_reset()
                elif choice == '5':
                    self.get_account_info()
                else:
                    print(f"{Fore.RED}{EMOJI['ERROR']} Invalid choice. Please enter 0-5{Style.RESET_ALL}")
                
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                self.clear_screen()
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.CYAN}{EMOJI['INFO']} Interrupted by user. Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}{EMOJI['ERROR']} Error: {str(e)}{Style.RESET_ALL}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
                self.clear_screen()


def main():
    """Entry point"""
    print(f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           🚀 Cursor Simple - Lightweight Tool 🚀         ║
║                   Version 1.3.0                          ║
║                                                           ║
║  Cross-Platform Support: Windows | macOS | Linux         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """)
    
    app = CursorSimple()
    app.run()


if __name__ == "__main__":
    main()

