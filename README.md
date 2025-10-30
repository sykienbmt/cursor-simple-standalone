# 🚀 Cursor Simple - Standalone Version

A lightweight, cross-platform tool to manage Cursor IDE authentication and machine ID.

![Version](https://img.shields.io/badge/version-1.3.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-Windows%20|%20macOS%20|%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-Educational-orange)

## ✨ Features

- ❌ **Quit Cursor** - Terminate Cursor IDE process
- 🔄 **Reset Machine ID** - Generate new machine ID for trial reset  
- 🔑 **Quick Update Token** - Auto-fetch & update (no confirmations!)
- ⚡ **Quick Reset** - Full reset: Machine ID + Token (fully automated!)
- 👤 **Get Account Info** - Display full account details (username, password, token)
- 🌐 **API Integration** - Fetch tokens from Google Apps Script API
- 🧹 **Auto Clear** - Clean terminal after each operation
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux
- 📦 **Lightweight** - Minimal dependencies (colorama, requests)
- 🎯 **Standalone** - No browser required

---

## ⚡ Quick Start (One Command!)

### 🚀 Run Instantly (No Installation)

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/start.ps1 | iex
```

**Linux / macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/start.sh | bash
```

This will:
- ✅ Download tool to temp folder
- ✅ Install dependencies
- ✅ Run immediately
- ✅ Auto-cleanup after exit

### 💾 Or Install Permanently

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.ps1 | iex
```

**Linux / macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.sh | bash
```

This will:
- ✅ Auto-detects/installs Python
- ✅ Downloads all files from GitHub
- ✅ Installs dependencies
- ✅ Installs to `%USERPROFILE%\cursor-simple-standalone` (Windows) or `~/cursor-simple-standalone` (Linux/macOS)

See [scripts/README.md](scripts/README.md) for more details.

---

## 📂 After Installation - Quick Start

### Windows
```powershell
cd $env:USERPROFILE\cursor-simple-standalone
START.bat
```

### macOS / Linux
```bash
cd ~/cursor-simple-standalone
./START.sh
```

**That's it!** The script will:
- ✅ Auto-install dependencies (first time)
- ✅ Launch the tool
- ✅ Display current account info on screen
- ✅ No manual setup needed

### 📺 What You'll See:

```
============================================================
📋 Cursor Simple - Cross-Platform Tool
============================================================

📧 Email: katrinaDixong4e92@oficial.us
📋 Subscription: Free_trial (trialing)
⏳ Remaining Pro Trial: 2 days
────────────────────────────────────────────────────────────

1. ❌ Quit Cursor
2. 🔄 Reset Machine ID
3. 🔑 Quick Update Token (Auto)
4. ✅ Quick Reset (Machine ID + Token)
5. 👤 Get Account Info (from API)
0. ❌ Exit
```

See [DEMO_OUTPUT.md](DEMO_OUTPUT.md) for full output examples.

---

## 📦 Manual Installation (Optional)

If you prefer manual setup:

```bash
# Install dependencies
pip install -r requirements.txt

# Or install manually
pip install colorama requests
```

**Note**: 
- `colorama` is optional (for colored output)
- `requests` is required for API integration (auto-fetch tokens)

## 🚀 Manual Usage (Optional)

```bash
# Run the tool directly
python cursor_simple.py

# Or make it executable (Linux/macOS)
chmod +x cursor_simple.py
./cursor_simple.py
```

## 📋 Menu Options

```
============================================================
📋 Cursor Simple - Cross-Platform Tool
============================================================

1. ❌ Quit Cursor
2. 🔄 Reset Machine ID
3. 🔑 Quick Update Token (Auto)
4. ✅ Quick Reset (Machine ID + Token)
5. 👤 Get Account Info
0. ❌ Exit
```

### 1. Quit Cursor
Terminates all running Cursor processes.

### 2. Reset Machine ID
Generates a new UUID and updates:
- Machine ID file
- storage.json
- SQLite database

**Use Case**: Reset free trial period

### 3. Quick Update Token ⚡ (FAST!)
**Fully automated token update - no confirmations!**

Automatically performs:
1. ✅ Fetch token from API
2. ✅ Refresh via Cursor server
3. ✅ Update database
4. ✅ Display account info

**Perfect for:**
- Quick token refresh
- Account switching
- Fast updates

**No user input needed** - just press 3!

**Output:**
```
============================================================
✅ Token Updated Successfully!
============================================================
Account Information:
├─ Email: example@email.com
├─ Password: password123
└─ Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
============================================================
```

### 4. Quick Reset ⚡ (FULL RESET)
**One-click full reset - no confirmations required!**

Automatically performs:
1. ✅ Quit Cursor
2. ✅ Reset Machine ID
3. ✅ Fetch new token from API
4. ✅ Refresh token via Cursor server
5. ✅ Update database

**Perfect for:**
- Fast account switching
- Quick trial resets
- Automated workflows

**No user input needed** - just press 4 and wait!

### 5. Get Account Info 👤 (VIEW ONLY)
**Display full account information without updating anything**

Automatically performs:
1. ✅ Fetch account from API
2. ✅ Refresh token via Cursor server
3. ✅ Display all information

**Shows:**
- Row number from API
- Username/Email
- Password
- Full token (with prefix)
- Access token (refreshed)

**Perfect for:**
- Checking account details
- Verifying tokens
- Getting credentials without modifying anything

**No changes made** - just displays information!

**Output:**
```
============================================================
👤 Account Information
============================================================

Row Number: 42
────────────────────────────────────────────────────────────

Username/Email:
  example@email.com

Password:
  password123

Full Token (with prefix):
  user_01K8B61KGN40J168E0KMZKY0CH%3A%3AeyJhbGc...

Access Token (refreshed):
  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

============================================================
✅ Account information displayed successfully!
============================================================
```

## 🔑 How to Get Token

### Method 1: Auto-fetch from API (Recommended)

The tool can automatically fetch tokens from a Google Apps Script API.

**Default API**: Included in the tool (option 1 when updating token)

**Custom API Setup**:
1. Create a Google Sheet with token data
2. Deploy a Google Apps Script Web App
3. Use the deployment URL when prompted

**API Response Format**:
```json
{
  "success": true,
  "data": {
    "token": "user_01K8B61KGN40J168E0KMZKY0CH%3A%3AeyJhbGc...",
    "account": "email@example.com/password123"
  },
  "row": 30
}
```

See `README_TokenAPI.md` for API setup instructions.

### Method 2: From Browser

1. Login to https://www.cursor.com
2. Open DevTools (F12)
3. Go to: Application → Cookies
4. Find: `WorkosCursorSessionToken`
5. Copy the entire value

### Method 3: From Another Machine

```bash
# Extract from SQLite database
sqlite3 <path-to-state.vscdb> \
  "SELECT value FROM ItemTable WHERE key='cursorAuth/accessToken'"
```

**Paths**:
- Windows: `%APPDATA%\Cursor\User\globalStorage\state.vscdb`
- macOS: `~/Library/Application Support/Cursor/User/globalStorage/state.vscdb`
- Linux: `~/.config/Cursor/User/globalStorage/state.vscdb`

## 💡 Example Workflow

```bash
# 1. Reset trial + Update token

python cursor_simple.py

# Choose 2: Reset Machine ID
# → Cursor closes
# → New machine ID generated

# Choose 3: Update Token
# → Paste your token
# → Enter email (or skip)
# → Confirm

# Choose 0: Exit

# Restart Cursor → Done!
```

## 🗂️ File Locations

### Windows
```
SQLite:     %APPDATA%\Cursor\User\globalStorage\state.vscdb
Storage:    %APPDATA%\Cursor\User\globalStorage\storage.json
Machine ID: %APPDATA%\Cursor\machineId
```

### macOS
```
SQLite:     ~/Library/Application Support/Cursor/User/globalStorage/state.vscdb
Storage:    ~/Library/Application Support/Cursor/User/globalStorage/storage.json
Machine ID: ~/Library/Application Support/Cursor/machineId
```

### Linux
```
SQLite:     ~/.config/Cursor/User/globalStorage/state.vscdb
Storage:    ~/.config/Cursor/User/globalStorage/storage.json
Machine ID: ~/.config/Cursor/machineid
```

## 🆘 Troubleshooting

### Windows: Python not installed? ⚡

**No problem! The script will AUTO-INSTALL Python for you!**

When you run `START.bat` for the first time without Python:
1. ✅ Script detects Python is missing
2. ✅ **Automatically installs Python via winget** (Windows 10/11)
3. ✅ Or opens browser to download if winget unavailable
4. ✅ Run `START.bat` again - done!

**Auto-install process:**
```
⚠️  Python not found! Attempting auto-install...
✓ Found winget! Installing Python automatically...
This may take a few minutes...
✅ Python installed successfully!
Please run START.bat again!
```

**If manual install needed:**
- Just tick "Add Python to PATH" during installation
- Restart terminal and run again

**The script includes:**
- ✅ **Auto-install Python via winget**
- ✅ Auto-detection (`py`, `python`, `python3`)
- ✅ Auto-install pip if missing
- ✅ Smart error handling

### "ModuleNotFoundError: colorama"
```bash
pip install colorama
# or
py -m pip install colorama
```
Or run without colors (tool still works).

### "Permission denied"
```bash
# Linux/macOS
sudo python cursor_simple.py

# Windows
# Run as Administrator
```

### "Database is locked"
- Make sure Cursor is closed
- Tool automatically quits Cursor
- Manually kill if needed: `pkill -9 cursor`

## 🎯 Requirements

- Python 3.7+
- colorama (optional)
- SQLite3 (included in Python)

## 📄 License

Educational purposes only. Please support the original Cursor IDE.

## 🙏 Credits

Part of the Cursor Free VIP community project.

---

## 🔄 Update

To update to the latest version, just run the one-click installer again!

**Windows:**
```powershell
irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.ps1 | iex
```

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.sh | bash
```

---

**Version**: 1.3.0  
**Last Updated**: 2025-10-30

**What's New in 1.3.0:**
- 📺 **Real-time Account Display** - Shows current email, subscription, and remaining days on main screen
- 👤 Added "Get Account Info" feature - view full account details from API
- 🚀 One-click installation scripts
- 🎨 Color-coded remaining days indicator (Green > Yellow > Red)
- 📝 Improved documentation with demo output examples

