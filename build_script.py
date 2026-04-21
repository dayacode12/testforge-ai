#!/usr/bin/env python3
"""
Simulated build script with intentional errors
Jenkins will run this and capture failures
"""
import sys
import time

def test_feature_auth():
    """Test authentication feature - HAS A BUG"""
    print("🔍 Testing authentication feature...")
    time.sleep(1)
    
    # Intentional bug: wrong import
    try:
        from utils import auth_helper  # This module doesn't exist
        user = auth_helper.authenticate("user", "pass")
    except ImportError as e:
        print(f"❌ ERROR: {e}")
        return False
    return True

def test_database_connection():
    """Test database connection - HAS A BUG"""
    print("🔍 Testing database connection...")
    time.sleep(1)
    
    # Intentional bug: connection string malformed
    db_url = "postgresql://localhost:5432/testdb"
    try:
        # Simulate connection that fails due to bad config
        if "localhost" in db_url and "testdb" not in db_url:
            raise Exception("Database configuration error: missing database name")
        # This line never executes due to bug above
        print("✓ Connected to database")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False
    return True

def test_api_response():
    """Test API response parsing - HAS A BUG"""
    print("🔍 Testing API response parsing...")
    time.sleep(1)
    
    # Intentional bug: incorrect JSON parsing
    response_data = '{"status": "ok", "data": [1, 2, 3]}'
    try:
        # Bug: trying to access non-existent key
        result = response_data['status']  # String, not dict!
    except TypeError as e:
        print(f"❌ ERROR: Cannot parse response - {e}")
        return False
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Starting automated test suite...")
    print("=" * 60)
    
    results = []
    results.append(test_feature_auth())
    results.append(test_database_connection())
    results.append(test_api_response())
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)
    
    sys.exit(0 if all(results) else 1)
