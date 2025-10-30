# 🚀 Cursor Simple v2.0 - Enhanced Edition

## ✨ Tính năng mới trong phiên bản 2.0.0

### 📅 JWT Token Decoder - Hiển thị chính xác ngày hết hạn
**Vấn đề cũ**: Không hiển thị được ngày hết hạn chính xác của token.

**Giải pháp mới**:
- Decode JWT token để lấy thời gian hết hạn chính xác
- Hiển thị ngày giờ hết hạn cụ thể (YYYY-MM-DD HH:MM:SS)
- Tính toán số ngày còn lại tự động
- Cảnh báo màu sắc (Xanh > 7 ngày, Vàng 2-7 ngày, Đỏ < 2 ngày)

### 🔑 Cải thiện Token Update
**Cải tiến**:
- Tự động đóng Cursor trước khi cập nhật token
- Đảm bảo token được áp dụng ngay lập tức
- Không cần thao tác thủ công


---

## 📋 Menu Chính

```
============================================================
📋 Cursor Simple - Cross-Platform Tool
============================================================

📧 Email: example@cursor.com
📋 Subscription: Free_trial (active)
⏳ Remaining Days: 15 days
📅 Expires At: 2025-11-14 15:30:45
────────────────────────────────────────────────────────────

1. ❌ Quit Cursor
2. 🔄 Reset Machine ID
3. 🔑 Quick Update Token (Auto)
4. ✅ Quick Reset (Machine ID + Token)
5. 👤 Get New Account (from API)
0. ❌ Exit
```

---

## 🔑 Chi tiết các chức năng

### Option 3: Quick Update Token - 2 Chế độ

Khi chọn option 3, bạn sẽ được hỏi chọn chế độ:

#### **Chế độ 1: Standard (Tiêu chuẩn)**
```
1. Đóng Cursor
2. Lấy token từ API
3. Cập nhật vào database
4. Bạn cần mở lại Cursor
```
✅ Phù hợp khi: Muốn đảm bảo 100% token được áp dụng ngay

#### **Chế độ 2: Seamless (Mượt mà) ⭐ RECOMMENDED**
```
1. KHÔNG đóng Cursor
2. Lấy token từ API
3. Cập nhật vào database
4. Cursor tự động dùng token mới
```
✅ Phù hợp khi: 
- Đang làm việc với Cursor, không muốn đóng
- Thay đổi tài khoản nhanh
- Cập nhật token định kỳ

**QUAN TRỌNG**: Ở chế độ Seamless, Cursor sẽ KHÔNG yêu cầu bạn đăng nhập lại!

---

### Option 6: Auto Token Refresh (Watch Mode)

**Chức năng**:
- Tự động làm mới token theo khoảng thời gian
- Sử dụng Seamless Mode (không đóng Cursor)
- Giám sát thời gian hết hạn token
- Tự động refresh khi token sắp hết hạn

**Cách sử dụng**:
```
1. Chọn option 6
2. Chọn khoảng thời gian refresh:
   - 30 phút
   - 1 giờ
   - 2 giờ
   - 4 giờ
   - Custom
3. Để chạy, nhấn Ctrl+C để dừng
```

**Kết quả mẫu**:
```
============================================================
🔄 Auto Refresh Started
============================================================
Refresh Interval: 60 minutes
Mode: Seamless (Cursor stays running)
Press Ctrl+C to stop...

[Cycle 1] 2025-10-30 10:15:30
Current Email: user@cursor.com
Expires At: 2025-11-14 15:30:45
✓ Token valid for 15 more days

Refreshing token from API...
✅ Token Updated Successfully!
Account Information:
├─ Email: user@cursor.com
├─ Token: eyJhbGc...
├─ Expires: 2025-11-15 15:30:45
└─ Valid for: 16 days

Token updated seamlessly - Cursor will use new token automatically!

⏳ Next refresh in 60 minutes...
```

---

## 🆕 Hiển thị thông tin Token nâng cao

### Trước đây (v1.3.0):
```
📧 Email: user@cursor.com
📋 Subscription: Free_trial (trialing)
⏳ Remaining Pro Trial: Unknown
```

### Bây giờ (v2.0.0):
```
📧 Email: user@cursor.com
📋 Subscription: Free_trial (active)
⏳ Remaining Days: 15 days
📅 Expires At: 2025-11-14 15:30:45
```

**Cải tiến**:
- ✅ Decode JWT để lấy chính xác thời gian hết hạn
- ✅ Hiển thị ngày giờ cụ thể (không còn "Unknown")
- ✅ Tự động tính số ngày còn lại
- ✅ Màu sắc thông minh (Xanh/Vàng/Đỏ)

---

## 🔧 Kỹ thuật Implementation

### JWT Token Decoder
```python
def decode_jwt(self, token: str) -> Optional[Dict]:
    """Decode JWT Token to get payload information"""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding
        
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception:
        return None
```

### Seamless Token Update
**Key Insight**: 
- Cursor đọc token từ SQLite database `state.vscdb`
- Nếu update token trong database mà không đóng Cursor, Cursor sẽ tự động sử dụng token mới khi cần
- Điều quan trọng là phải update đúng các key:
  - `cursorAuth/accessToken`
  - `cursorAuth/refreshToken`
  - `cursorAuth/expiresAt` (với timestamp chính xác từ JWT)
  - `WorkosCursorSessionToken`

---

## 📊 So sánh v1.3.0 vs v2.0.0

| Tính năng | v1.3.0 | v2.0.0 |
|-----------|--------|---------|
| Hiển thị ngày hết hạn | ❌ "Unknown" | ✅ Chính xác đến giây |
| Update token không đóng Cursor | ❌ | ✅ Seamless Mode |
| Auto refresh token | ❌ | ✅ Watch Mode |
| Decode JWT | ❌ | ✅ Full decoder |
| Multi-mode update | ❌ | ✅ Standard + Seamless |
| Token expiry warning | ❌ | ✅ Màu sắc cảnh báo |

---

## 🎯 Use Cases

### 1. Developer đang code, muốn đổi tài khoản
```bash
Chọn option 3 → Chọn mode 2 (Seamless)
→ Token đổi ngay, không mất code đang làm
```

### 2. Kiểm tra xem token còn bao lâu hết hạn
```bash
Nhìn vào menu chính
→ Thấy ngay "📅 Expires At: 2025-11-14 15:30:45"
```

---

## 🚀 Quick Start

### Cài đặt
```bash
cd cursor-simple-standalone
pip install -r requirements.txt
python cursor_simple.py
```

### Cập nhật từ v1.3.0 lên v2.0.0
```bash
# Backup file cũ (optional)
cp cursor_simple.py cursor_simple_v1.3.0.py

# Pull code mới
git pull origin main

# Chạy
python cursor_simple.py
```

---

## ⚙️ Requirements

```
Python 3.7+
colorama (optional, for colors)
requests (required, for API calls)
```

---

## 📝 API Format

API cần trả về format:
```json
{
  "success": true,
  "data": {
    "token": "user_xxx%3A%3AeyJhbGc...",
    "account": "email@example.com/password123"
  },
  "row": 42
}
```

Token từ API sẽ được:
1. Refresh qua Cursor server để lấy `accessToken`
2. Decode JWT để lấy `exp` (expiry timestamp)
3. Lưu vào database với `expiresAt` chính xác

---

## 🐛 Troubleshooting

### "Token updated but Cursor still shows old account"
→ Đóng và mở lại Cursor (chỉ cần 1 lần)

### "Expires At: Unknown"
→ Token không phải JWT format hoặc không có `exp` field
→ Vẫn hoạt động bình thường, chỉ không hiển thị được expire time


---

## 🙏 Credits

- Original: Cursor Free VIP Community
- Enhanced by: Your contribution
- Inspired by: cursor-token project

---

## 📄 License

Educational Use Only. Support the original Cursor IDE.

---

**Version**: 2.0.0  
**Last Updated**: 2025-10-30  
**Status**: ✅ Production Ready

