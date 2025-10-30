#!/usr/bin/env python3
"""
Test script for Cursor Simple v2.0.0
Verify các tính năng mới hoạt động đúng
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from cursor_simple import CursorSimple
from datetime import datetime, timedelta

def test_jwt_decoder():
    """Test JWT decoder functionality"""
    print("\n" + "="*60)
    print("TEST 1: JWT Token Decoder")
    print("="*60)
    
    app = CursorSimple()
    
    # Sample JWT token (this is a test token, not real)
    test_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE3MzAzNzI2MDB9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    
    # Test decode
    print("\n1. Testing JWT decode...")
    payload = app.decode_jwt(test_token)
    
    if payload:
        print(f"✅ Decode successful!")
        print(f"   Payload: {payload}")
    else:
        print(f"❌ Decode failed!")
        return False
    
    # Test expiry extraction
    print("\n2. Testing expiry time extraction...")
    expire_time = app.get_token_expiry(test_token)
    
    if expire_time:
        print(f"✅ Expiry extraction successful!")
        print(f"   Expires at: {expire_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Calculate remaining time
        now = datetime.now()
        if expire_time > now:
            remaining = expire_time - now
            print(f"   Remaining: {app.format_timedelta(remaining)}")
        else:
            print(f"   Status: Expired")
    else:
        print(f"❌ Expiry extraction failed!")
        return False
    
    # Test timedelta formatting
    print("\n3. Testing timedelta formatting...")
    test_deltas = [
        timedelta(days=15, hours=3, minutes=30),
        timedelta(hours=5, minutes=15),
        timedelta(minutes=30),
        timedelta(seconds=45)
    ]
    
    for td in test_deltas:
        formatted = app.format_timedelta(td)
        print(f"   {td} → {formatted}")
    
    print("\n✅ All JWT decoder tests passed!")
    return True

def test_paths():
    """Test cursor paths detection"""
    print("\n" + "="*60)
    print("TEST 2: Cursor Paths Detection")
    print("="*60)
    
    app = CursorSimple()
    
    print(f"\nDetected system: {app.system}")
    print(f"\nCursor paths:")
    for key, path in app.paths.items():
        exists = "✅" if os.path.exists(path) else "❌"
        print(f"  {exists} {key}: {path}")
    
    print("\n✅ Paths test completed!")
    return True

def test_account_info():
    """Test account info retrieval"""
    print("\n" + "="*60)
    print("TEST 3: Account Info Retrieval")
    print("="*60)
    
    app = CursorSimple()
    
    print("\nAttempting to get current account info...")
    account_info = app.get_current_account_info()
    
    if account_info:
        print(f"✅ Account info retrieved successfully!")
        print(f"\n   Email: {account_info['email']}")
        print(f"   Subscription: {account_info['subscription']}")
        print(f"   Remaining Days: {account_info['remaining_days']}")
        print(f"   Expires At: {account_info.get('expire_time', 'Unknown')}")
    else:
        print(f"⚠️  No account info found (Cursor may not be installed or not logged in)")
    
    print("\n✅ Account info test completed!")
    return True

def test_token_storage():
    """Test token storage path"""
    print("\n" + "="*60)
    print("TEST 4: Token Storage")
    print("="*60)
    
    app = CursorSimple()
    
    print(f"\nToken storage path: {app.token_storage}")
    print(f"Parent directory: {app.token_storage.parent}")
    print(f"Exists: {app.token_storage.exists()}")
    
    print("\n✅ Token storage test completed!")
    return True

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("Cursor Simple v2.0.0 - Test Suite")
    print("="*70)
    
    tests = [
        ("JWT Decoder", test_jwt_decoder),
        ("Cursor Paths", test_paths),
        ("Account Info", test_account_info),
        ("Token Storage", test_token_storage)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! v2.0.0 is ready!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

