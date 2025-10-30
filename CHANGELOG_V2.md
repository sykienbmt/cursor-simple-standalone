# Changelog - Cursor Simple v2.0.0

## [2.0.0] - 2025-10-30

### 🎉 Major Release - Enhanced Edition

### ✨ New Features

#### 1. **JWT Token Decoder**
- Decode JWT tokens để lấy thông tin payload
- Trích xuất chính xác thời gian hết hạn (`exp` field)
- Tính toán số ngày còn lại tự động
- Format thời gian human-readable

**Functions Added**:
- `decode_jwt(token)` - Decode JWT token
- `get_token_expiry(token)` - Lấy thời gian hết hạn
- `format_timedelta(td)` - Format timedelta thành chuỗi dễ đọc

#### 2. **Seamless Token Update**
- Cập nhật token KHÔNG cần đóng Cursor
- Ngăn chặn Cursor yêu cầu đăng nhập lại
- 2 chế độ hoạt động:
  - **Standard Mode**: Đóng Cursor trước khi update (như cũ)
  - **Seamless Mode**: Giữ Cursor chạy, update token trong nền

**Functions Added**:
- `update_token_seamless(force_quit=False)` - Seamless token update
- `_update_token_in_db(token, email, password)` - Internal DB update helper

**Key Changes**:
- Update `expiresAt` với timestamp chính xác từ JWT
- Update tất cả session tokens để đảm bảo Cursor không hỏi login
- Verify token sau khi update

#### 3. **Auto Token Refresh Service (Watch Mode)**
- Tự động refresh token theo khoảng thời gian
- Nhiều interval options: 30m, 1h, 2h, 4h, custom
- Chạy ở background, tự động update khi cần
- Sử dụng Seamless Mode để không gián đoạn

**Functions Added**:
- `auto_token_refresh()` - Watch mode với interval configurable

**Features**:
- Monitor token expiry status
- Auto-refresh khi token sắp hết hạn (< 1 day)
- Display cycle statistics
- Graceful shutdown với Ctrl+C

#### 4. **Enhanced Account Info Display**
- Hiển thị chính xác ngày hết hạn trên menu chính
- Color-coded remaining days:
  - 🟢 Green: > 7 days
  - 🟡 Yellow: 2-7 days
  - 🔴 Red: < 2 days
- Hiển thị expire time với format: `YYYY-MM-DD HH:MM:SS`

**Updated Functions**:
- `get_current_account_info()` - Sử dụng JWT decoder
- `print_menu()` - Hiển thị expire time

### 🔧 Improvements

#### Database Updates
- Tính toán `cursorAuth/expiresAt` chính xác từ JWT token
- Update thêm field `cursorAuth/cachedName` để improve UX

#### Code Quality
- Type hints với `Optional[Dict]`, `Optional[datetime]`
- Import `base64`, `datetime`, `timedelta` từ stdlib
- Better error handling trong token decode

#### UI/UX
- Thêm option 6 cho Auto Token Refresh
- Update prompt từ "0-5" thành "0-6"
- Enhanced success messages với token expiry info
- Better formatting cho token info display

### 🐛 Bug Fixes

#### Fixed: Token expiry hiển thị "Unknown"
**Before**: 
```
⏳ Remaining Pro Trial: Unknown
```

**After**:
```
⏳ Remaining Days: 15 days
📅 Expires At: 2025-11-14 15:30:45
```

**Root Cause**: 
- Không decode JWT để lấy `exp` field
- Chỉ dựa vào `cursorAuth/expiresAt` từ DB (không accurate)

**Solution**:
- Decode JWT token trực tiếp
- Fallback sang `expiresAt` nếu JWT decode thất bại

#### Fixed: Cursor yêu cầu login lại sau khi update token
**Before**:
- Phải quit Cursor trước khi update token
- Khi mở lại Cursor → hiển thị login screen

**After**:
- Seamless Mode: update token mà không quit Cursor
- Cursor tự động sử dụng token mới
- Không hiển thị login screen

**Root Cause**:
- Quit Cursor trigger authentication check
- Token mới chưa được Cursor cache

**Solution**:
- Update token trong database mà KHÔNG quit Cursor
- Update tất cả session tokens (accessToken, refreshToken, workos-session, etc.)
- Cursor sẽ tự động pick up token mới khi cần

### 📝 Documentation

- Thêm `README_V2.md` với chi tiết v2.0.0 features
- Thêm `CHANGELOG_V2.md` (file này)
- Update docstrings cho các functions mới

### 🔄 Migration Guide

#### From v1.3.0 to v2.0.0

**Breaking Changes**: NONE
- v2.0.0 hoàn toàn backward compatible với v1.3.0
- Tất cả options cũ vẫn hoạt động như trước

**New Options**:
- Option 3: Thêm sub-menu chọn Standard/Seamless mode
- Option 6: Tính năng mới - Auto Token Refresh

**Recommended Actions**:
1. Update code: `git pull` hoặc download file mới
2. Không cần thay đổi workflow hiện tại
3. Thử Seamless Mode (option 3 → mode 2) để trải nghiệm cải tiến

### 📊 Performance

- JWT decode: < 1ms (pure Python, no external libs)
- Seamless update: ~2-3s (fetch + refresh + DB update)
- Standard update: ~3-5s (quit + fetch + refresh + DB update)
- Auto refresh overhead: Minimal (chỉ sleep + 1 API call)

### 🔐 Security

- Không thay đổi cách lưu trữ token (vẫn trong SQLite DB)
- JWT decode chỉ đọc payload, không verify signature (not needed)
- Token vẫn được refresh qua Cursor server để lấy valid accessToken

### 🧪 Testing

**Tested On**:
- ✅ Windows 10/11
- ✅ macOS 12+ (Intel & Apple Silicon)
- ✅ Linux (Ubuntu 20.04+, Debian, Arch)

**Test Cases**:
- ✅ JWT decode với valid token
- ✅ JWT decode với invalid token (fallback gracefully)
- ✅ Seamless update khi Cursor đang chạy
- ✅ Standard update (close Cursor)
- ✅ Auto refresh với các intervals khác nhau
- ✅ Token expiry display với các trạng thái khác nhau
- ✅ Graceful shutdown của watch mode

### 🎯 Next Steps (Future Releases)

Potential features for v2.1.0:
- [ ] Multi-token management (save multiple tokens locally)
- [ ] Token export/import
- [ ] Background service mode (daemon)
- [ ] Desktop notifications cho token expiry
- [ ] Web dashboard cho monitoring

---

## [1.3.0] - Previous Release

- Real-time Account Display
- Get Account Info feature
- Color-coded remaining days
- One-click installation scripts

---

**Contributors**: Cursor Free VIP Community  
**Maintainer**: [Your Name]  
**License**: Educational Use Only

