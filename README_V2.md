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

### Option 3: Quick Update Token

**Chức năng**:
```
1. Đóng Cursor
2. Lấy token từ API
3. Refresh token qua Cursor server
4. Cập nhật vào database
5. Hiển thị thông tin tài khoản
```

**Đặc điểm**:
- ✅ Tự động đóng Cursor trước khi cập nhật
- ✅ Đảm bảo token được áp dụng 100%
- ✅ Không cần nhập gì, hoàn toàn tự động
- ✅ Hiển thị email, password, token ngay sau khi update

**Lưu ý**: Phải đóng Cursor trước khi update token để tránh conflict database

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

### Token Update Process
**Cách thức hoạt động**: 
- Cursor đọc token từ SQLite database `state.vscdb`
- Phải đóng Cursor trước khi update để tránh database lock
- Update các key quan trọng:
  - `cursorAuth/accessToken`
  - `cursorAuth/refreshToken`
  - `cursorAuth/expiresAt` (với timestamp chính xác từ JWT)
  - `WorkosCursorSessionToken`

---

## 📊 So sánh v1.3.0 vs v2.0.0

| Tính năng | v1.3.0 | v2.0.0 |
|-----------|--------|---------|
| Hiển thị ngày hết hạn | ❌ "Unknown" | ✅ Chính xác đến giây |
| Decode JWT | ❌ | ✅ Full decoder |
| Token expiry warning | ❌ | ✅ Màu sắc cảnh báo |
| Tự động đóng Cursor | ❌ Thủ công | ✅ Tự động |
| Hiển thị expiry datetime | ❌ | ✅ YYYY-MM-DD HH:MM:SS |
| Tính số ngày còn lại | ❌ Manual | ✅ Tự động từ JWT |

---

## 🎯 Use Cases

### 1. Cần đổi tài khoản mới
```bash
Chọn option 3 (Quick Update Token)
→ Tự động đóng Cursor, lấy token mới, update database
→ Mở lại Cursor với tài khoản mới
```

### 2. Reset toàn bộ (Machine ID + Token)
```bash
Chọn option 4 (Quick Reset)
→ Tự động reset Machine ID và update token
→ Mở lại Cursor là xong
```

### 3. Kiểm tra xem token còn bao lâu hết hạn
```bash
Nhìn vào menu chính
→ Thấy ngay "📅 Expires At: 2025-11-14 15:30:45"
→ "⏳ Remaining Pro Trial: 15 days"
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

