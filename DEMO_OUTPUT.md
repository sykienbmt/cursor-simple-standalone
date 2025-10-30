# 🎬 Demo Output - Cursor Simple v1.3.0

## Main Menu Display

Khi bạn chạy tool, bạn sẽ thấy:

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║           🚀 Cursor Simple - Lightweight Tool 🚀         ║
║                   Version 1.3.0                          ║
║                                                           ║
║  Cross-Platform Support: Windows | macOS | Linux         ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

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

System: Windows
SQLite Path: C:\Users\...\AppData\Roaming\Cursor\User\globalStorage\state.vscdb

➜ Enter choice (0-5): 
```

## Features:

### 🎯 Current Account Display
- **Email** - Hiển thị email đang đăng nhập
- **Subscription** - Loại subscription (Free_trial, Pro, etc.)
- **Remaining Days** - Số ngày còn lại (với màu sắc thay đổi theo số ngày)
  - 🟢 Green: > 7 days
  - 🟡 Yellow: 3-7 days
  - 🔴 Red: < 3 days

### 📊 Status Indicators:
- ✅ **Logged in**: Hiển thị đầy đủ thông tin
- ⚠️ **Not logged in**: Hiển thị "Not logged in"
- 🔄 **Unknown**: Không thể lấy thông tin token

---

## Option 5: Get Account Info (from API)

Khi chọn option 5:

```
👤 Get Account Information
============================================================

ℹ️  Fetching account from API...

✅ Token fetched successfully!
============================================================
Row: 42
Email: example@email.com
Token (first 50 chars): user_01K8B61KGN40J168E0KMZKY0CH%3A%3AeyJhbGc...
============================================================

ℹ️  Refreshing token via Cursor server...
✅ Token refreshed successfully!
├─ Valid for: 15 days
└─ Expires: 2025-11-15

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
  user_01K8B61KGN40J168E0KMZKY0CH%3A%3AeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Access Token (refreshed):
  eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6...

============================================================
✅ Account information displayed successfully!
============================================================
```

---

## Color Coding

- 🟢 **Green** - Success messages, > 7 days remaining
- 🟡 **Yellow** - Warning messages, 3-7 days remaining, menu options
- 🔴 **Red** - Error messages, < 3 days remaining
- 🔵 **Cyan** - Info messages, separators
- ⚪ **White** - Normal text

---

**Version**: 1.3.0  
**Last Updated**: 2025-10-30

