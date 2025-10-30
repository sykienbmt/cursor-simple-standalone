# Changelog

All notable changes to Cursor Simple will be documented in this file.

## [1.2.0] - 2025-10-29

### Fixed
- 🔧 **CRITICAL FIX**: Reset Machine ID now works correctly
- Now generates 4 different IDs (devDeviceId, machineId, macMachineId, sqmId)
- Updates all 5 keys in storage.json and SQLite database
- Updates Windows Registry MachineGuid (Windows only)

### Technical
- Added `_generate_machine_ids()` - generates all required IDs using secrets module
- Added `_update_windows_registry()` - updates Windows Registry (optional)
- Updated `reset_machine_id()` and `quick_reset()` to use comprehensive reset logic

---

## [1.1.4] - 2025-10-29

### Fixed
- 🔧 **CRITICAL FIX**: Increased API timeout from 10s → 60s for Google Apps Script
- 🔁 **Auto Retry**: Added 3-attempt retry logic with smart delays
  - Timeout errors: 5 second delay before retry
  - Other errors: 3 second delay before retry
  - Clear progress messages for each attempt
- Resolved "Request timeout" error when fetching tokens from Google Sheets

### Technical
- Google Apps Script can take 15-30 seconds (cold start + sheet operations)
- Retry logic handles transient network issues
- Better error messages showing retry progress

### Why This Fix Matters
- Users reported: "Sheet đã đổi trạng thái nhưng vẫn bị timeout"
- Root cause: API response took > 10 seconds
- Solution: 60s timeout + 3 retries = reliable token fetching

---

## [1.1.3] - 2025-10-29

### Added
- 🔍 **Verbose Logging** - Enhanced debugging output
  - Shows token before/after refresh
  - Displays each database key update
  - Verifies token saved in database
  - Helps troubleshoot login issues

### Enhanced
- Better visibility into token refresh process
- Database verification after update
- More detailed progress messages

### Technical
- Added logging for token comparison (before/after refresh)
- Added database read-back verification
- Each UPDATE operation now shows confirmation

---

## [1.1.2] - 2025-10-29

### Fixed
- 🔧 **CRITICAL FIX**: Option 3 now closes Cursor before updating token
- Fixed token not working after update (database was locked by running Cursor)
- This matches original project behavior where Cursor must be closed first

### Enhanced
- Option 3 now shows progress: Step 1/3, 2/3, 3/3
- Better messaging after token update
- Both Option 3 and Option 4 now display password in account info

### Technical
- `update_token()` now calls `quit_cursor()` before updating database
- Ensures database is not locked during write operations
- Tokens now work immediately without requiring re-login

---

## [1.1.1] - 2025-10-29

### Added
- ✨ **Quick Update Token** - Option 3 now fully automated!
  - No confirmations required
  - Auto-fetch from API → Refresh → Update → Display account info
  - Shows email/password after update
- ✨ **Quick Reset** - New option 4: Reset Machine ID + Update Token in one go
  - No confirmations required
  - Fully automated: Quit Cursor → Reset Machine ID → Fetch & Update Token
  - Perfect for fast account switching
- 🧹 **Auto Clear Screen** - Terminal clears after each operation for cleaner UI

### Changed
- **Option 3 simplified**: No more choosing between API/Manual
- **Option 3 now auto-only**: Always fetches from API, zero clicks needed
- Removed all confirmation prompts from option 3
- Better account info display with email/password

### Fixed
- 🔧 **CRITICAL FIX**: Added token refresh via Cursor API server
- Now properly refreshes tokens through `https://token.cursorpro.com.cn/reftoken`
- Tokens now work immediately without requiring re-login
- Matches the behavior of original project

### Enhanced
- Menu now shows "Quick Update Token (Auto)" for option 3
- Menu now shows "Quick Reset (Machine ID + Token)" for option 4
- Better UX with automatic screen clearing between operations
- Progress indicators for Quick Reset ([1/3], [2/3], [3/3])
- Cleaner account info output with tree-style formatting

### Technical
- Added `refresh_cursor_token()` method to refresh tokens via Cursor server
- Added `clear_screen()` method for cross-platform terminal clearing
- Added `quick_reset()` method for automated full reset
- Auto-refresh for both API-fetched and manually-entered tokens
- Displays token validity period and expiration date
- Proper error handling with fallback to original token if refresh fails

### Why This Was Needed
The original project always refreshes tokens through Cursor's API server before using them. Without this step, tokens would require a re-login on first use. This update ensures tokens work immediately after update.

---

## [1.1.0] - 2025-10-29

### Added
- 🌐 **API Integration**: Auto-fetch tokens from Google Apps Script API
- Two-mode token update: Auto-fetch or Manual input
- Account information display (email/password) when fetching from API
- Custom API URL support
- `requests` library dependency for HTTP requests

### Enhanced
- **Update Token** now offers choice between:
  - Option 1: Auto-fetch from API (with account info display)
  - Option 2: Manual input (original method)
- Better user experience with detailed token information
- API error handling and timeout support

### Changed
- Updated `requirements.txt` to include `requests>=2.28.0`
- Enhanced documentation with API setup guide
- Updated README.md with API integration examples
- Updated QUICKSTART.md with auto-fetch workflow

### Technical
- Added `fetch_token_from_api()` method
- Improved token parsing for both API and manual methods
- JSON response parsing with validation
- HTTP request error handling (timeout, network errors)

## [1.0.0] - 2025-10-29

### Added
- Initial standalone release
- Cross-platform support (Windows, macOS, Linux)
- Quit Cursor functionality
- Reset Machine ID functionality
- Update Token functionality
- Automatic token extraction from cookie format
- Optional colorama dependency for colored output
- Fallback to plain text if colorama not available
- Comprehensive error handling
- User-friendly menu interface

### Features
- **Quit Cursor**: Terminate Cursor IDE process on all platforms
- **Reset Machine ID**: Generate new UUID and update all locations
  - Machine ID file
  - storage.json
  - SQLite database (state.vscdb)
- **Update Token**: Manually input authentication token
  - Supports multiple token formats
  - Optional email input
  - Confirmation before update
  - Updates all auth keys in database

### Documentation
- README.md with full documentation
- QUICKSTART.md for quick start guide
- LICENSE file for educational use
- .gitignore for clean repository

### Technical
- Python 3.7+ compatibility
- Minimal dependencies (only colorama, optional)
- ~350 lines of clean, documented code
- Standalone script, no complex setup required

### Platform Support
- ✅ Windows (tested)
- ✅ macOS (tested)
- ✅ Linux (tested)

---

## Future Plans

### [1.1.0] - Planned
- [ ] Backup and restore functionality
- [ ] Token validation before update
- [ ] Batch operations mode
- [ ] Configuration file support
- [ ] Verbose/debug mode

### [1.2.0] - Planned
- [ ] GUI version (Tkinter/PyQt)
- [ ] Auto-detect token from running Cursor
- [ ] Export/import settings
- [ ] Multiple profile management

---

**Note**: This is a standalone version focused on simplicity and minimal dependencies.

