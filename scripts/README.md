# 🚀 Cursor Simple - One-Click Scripts

Run or install Cursor Simple with just one command!

## ⚡ Quick Start (Run Instantly)

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/start.ps1 | iex
```

**What it does:**
- ✅ Downloads to temp folder
- ✅ Runs immediately
- ✅ Auto-cleanup after exit
- ✅ No installation needed

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/start.sh | bash
```

**What it does:**
- ✅ Downloads to `/tmp`
- ✅ Runs immediately
- ✅ Auto-cleanup after exit
- ✅ No installation needed

---

## 💾 Or Install Permanently

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.ps1 | iex
```

**What it does:**
- ✅ Auto-detects or installs Python
- ✅ Downloads all required files from GitHub
- ✅ Installs dependencies automatically
- ✅ Asks if you want to run the tool immediately
- ✅ Installs to: `%USERPROFILE%\cursor-simple-standalone`

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.sh | bash
```

**What it does:**
- ✅ Checks Python installation
- ✅ Downloads all required files from GitHub
- ✅ Installs dependencies automatically
- ✅ Makes scripts executable
- ✅ Asks if you want to run the tool immediately
- ✅ Installs to: `~/cursor-simple-standalone`

---

## 📋 What Gets Installed

The installer downloads:
- `cursor_simple.py` - Main tool
- `requirements.txt` - Python dependencies
- `START.bat` - Windows quick launcher
- `START.sh` - Linux/macOS quick launcher
- `install.bat` - Local installer (Windows)
- `install.sh` - Local installer (Linux/macOS)
- `README.md` - Documentation
- `QUICKSTART.md` - Quick start guide
- `LICENSE` - License file

---

## 🎯 After Installation

### Run from installation directory

**Windows:**
```powershell
cd $env:USERPROFILE\cursor-simple-standalone
python cursor_simple.py

# Or double-click:
START.bat
```

**Linux/macOS:**
```bash
cd ~/cursor-simple-standalone
python3 cursor_simple.py

# Or:
./START.sh
```

---

## 🔄 Update Installation

Just run the install command again! It will:
1. Remove old installation
2. Download latest files
3. Reinstall dependencies

---

## 🗑️ Uninstall

**Windows:**
```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\cursor-simple-standalone"
```

**Linux/macOS:**
```bash
rm -rf ~/cursor-simple-standalone
```

---

## 🆘 Troubleshooting

### Windows: "Running scripts is disabled"

Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run the install command again.

### "Python not found"

**Windows:**
- The installer will attempt to auto-install Python via winget
- Or manually download from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip
```

### "Permission denied"

**Linux/macOS:**
```bash
chmod +x ~/cursor-simple-standalone/cursor_simple.py
chmod +x ~/cursor-simple-standalone/START.sh
```

### "curl: command not found"

**Windows:** Use PowerShell command instead  
**Linux:** `sudo apt install curl` or `sudo yum install curl`

---

## 🔐 Security Note

These scripts download files from GitHub. You can:
1. Review the scripts before running (they're open source)
2. Download and inspect manually
3. Fork the repository and use your own URL

---

## 📄 License

Educational purposes only. Please support the original Cursor IDE.

---

**Repository:** https://github.com/sykienbmt/cursor-simple-standalone

