# 🚀 Quick Start - Cursor Simple

**Chỉ cần 1 lệnh duy nhất!**

---

## 🚀 RUN INSTANTLY (Không cần cài đặt!)

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/sykienbmt/simple-standalone/HEAD/scripts/start.ps1 | iex
```

### Linux/macOS
```bash
curl -fsSL https://raw.githubusercontent.com/sykienbmt/simple-standalone/HEAD/scripts/start.sh | bash
```

**Chạy ngay lập tức!**
- ✅ Tải về temp folder
- ✅ Chạy tool
- ✅ Tự động dọn dẹp sau khi thoát
- ✅ Không cần cài đặt gì cả!

---

## 💾 HOẶC CÀI ĐẶT VÀO MÁY

### Windows (PowerShell)
```powershell
irm https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.ps1 | iex
```

### Linux/macOS
```bash
curl -fsSL https://raw.githubusercontent.com/sykienbmt/cursor-simple-standalone/HEAD/scripts/install.sh | bash
```

**Cài đặt vĩnh viễn vào máy!**
- ✅ Cài vào `%USERPROFILE%\cursor-simple-standalone` (Windows)
- ✅ Hoặc `~/cursor-simple-standalone` (Linux/macOS)
- ✅ Chạy bất cứ lúc nào với `START.bat` hoặc `./START.sh`

---

## ⚡ SAU KHI CÀI ĐẶT - FASTEST WAY

### Cách 1: Chỉ Update Token (3 giây)
```powershell
cd $env:USERPROFILE\cursor-simple-standalone  # Windows
# hoặc: cd ~/cursor-simple-standalone         # Linux/macOS

START.bat  # Windows
# hoặc: ./START.sh  # Linux/macOS

# Chọn: 3 (Quick Update Token)
# Xong! Tự động fetch và hiển thị account/pass
```

### Cách 2: Full Reset (10 giây)
```powershell
cd $env:USERPROFILE\cursor-simple-standalone  # Windows
# hoặc: cd ~/cursor-simple-standalone         # Linux/macOS

START.bat  # Windows
# hoặc: ./START.sh  # Linux/macOS

# Chọn: 4 (Quick Reset)
# Xong! Reset Machine ID + Token tự động
```

---

**Option 3 - Quick Update Token** (Super Fast!):
- ✅ Fetch token từ API
- ✅ Refresh qua Cursor server
- ✅ Update database
- ✅ Hiển thị email/password
- ⚡ Không cần confirm gì!

**Option 4 - Quick Reset** (Full Reset):
1. ✅ Đóng Cursor
2. ✅ Reset Machine ID
3. ✅ Lấy token mới
4. ✅ Update database
5. ✅ Không cần confirm gì!

---

## 🪟 Windows

### Cách 1: Double-click (Dễ nhất)
1. Double-click file `START.bat`
2. Chọn tính năng bạn muốn
3. Xong!

### Cách 2: Command Line
```powershell
START.bat
```

Xong! Script sẽ tự động:
- ✅ Kiểm tra Python
- ✅ Cài đặt dependencies (lần đầu)
- ✅ Chạy tool

---

## 🍎 macOS

### Chạy trong Terminal
```bash
./START.sh
```

Xong! Script sẽ tự động:
- ✅ Kiểm tra Python
- ✅ Cài đặt dependencies (lần đầu)
- ✅ Chạy tool

**Lưu ý**: Nếu báo lỗi permission, chạy:
```bash
chmod +x START.sh
./START.sh
```

---

## 🐧 Linux

### Chạy trong Terminal
```bash
./START.sh
```

Xong! Script sẽ tự động:
- ✅ Kiểm tra Python
- ✅ Cài đặt dependencies (lần đầu)
- ✅ Chạy tool

**Lưu ý**: Nếu báo lỗi permission, chạy:
```bash
chmod +x START.sh
./START.sh
```

---

## 📋 Menu Tool

Khi tool chạy, bạn sẽ thấy:

```
============================================================
📋 Cursor Simple - Cross-Platform Tool
============================================================

1. ❌ Quit Cursor
2. 🔄 Reset Machine ID
3. 🔑 Update Token
0. ❌ Exit

Enter your choice:
```

### Chọn Option 3: Update Token

Sau đó sẽ thấy:
```
Select token source:
  1. ➜ Auto-fetch from API
  2. ➜ Manual input

Enter choice (1 or 2):
```

**Chọn 1** để tự động lấy token từ API:
- Nhập `1`
- Nhập `y` (dùng API mặc định)
- Token sẽ tự động fetch và hiển thị thông tin account
- Nhập `y` để xác nhận
- ✅ Xong!

---

## 🎯 Full Workflow (Khuyến nghị)

### Windows
```powershell
# Bước 1: Double-click START.bat

# Bước 2: Chọn 1 (Quit Cursor)

# Bước 3: Chạy lại START.bat

# Bước 4: Chọn 2 (Reset Machine ID)

# Bước 5: Chạy lại START.bat

# Bước 6: Chọn 3 → 1 → y → y (Update Token từ API)

# Bước 7: Restart Cursor
```

### macOS / Linux
```bash
# Bước 1: Chạy tool
./START.sh

# Bước 2: Chọn 1 (Quit Cursor)

# Bước 3: Chạy lại
./START.sh

# Bước 4: Chọn 2 (Reset Machine ID)

# Bước 5: Chạy lại
./START.sh

# Bước 6: Chọn 3 → 1 → y → y (Update Token từ API)

# Bước 7: Start Cursor
```

---

## 🔧 Nếu Có Lỗi

### Windows

**❌ Python chưa cài đặt?**

**Không lo! Script sẽ TỰ ĐỘNG TẢI VÀ CÀI Python cho bạn!**

Khi chạy `START.bat` lần đầu, script sẽ:
1. ✅ Phát hiện Python chưa có
2. ✅ **Tự động cài qua winget** (Windows 10/11)
3. ✅ **Hoặc tự động tải installer và cài đặt** (Windows 7/8)
4. ✅ Không cần làm gì! Chỉ chạy lại `START.bat` là xong!

**Quá trình HOÀN TOÀN TỰ ĐỘNG:**
```
⚠️  Python not found! Attempting auto-install...
Downloading Python 3.11.9 (this may take a few minutes)...
✓ Download complete! Installing Python...
✅ Python installation completed!
Please run START.bat again!
```

**Bạn không cần làm GÌ CẢ!** Script lo tất cả:
- ✅ Tải Python installer (~30MB)
- ✅ Cài đặt tự động (silent install)
- ✅ Thêm vào PATH tự động
- ✅ Cài pip tự động

**Dependencies lỗi?**
```powershell
# Cài thủ công
py -m pip install colorama requests
```

### macOS

**Python không có?**
```bash
# Cài qua Homebrew
brew install python3
```

**Permission denied?**
```bash
chmod +x START.sh
```

### Linux

**Python không có?**
```bash
# Ubuntu/Debian
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

**Permission denied?**
```bash
chmod +x START.sh
```

---

## ⚡ Tóm Tắt

| Platform | Lệnh Chạy | Yêu Cầu |
|----------|-----------|---------|
| **Windows** | `START.bat` (double-click) | Python 3.7+ |
| **macOS** | `./START.sh` | Python 3 (có sẵn) |
| **Linux** | `./START.sh` | Python 3 + pip |

**Tất cả đều tự động cài dependencies!**

---

## 📚 Thông Tin Thêm

- **README.md** - Tài liệu đầy đủ
- **CHANGELOG.md** - Lịch sử phiên bản

---

## ✅ That's It!

**Chỉ cần chạy START.bat (Windows) hoặc START.sh (macOS/Linux) là xong!** 🎉
