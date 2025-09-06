#!/usr/bin/env python3
"""
Security Testing Script for Django Healthcare Backend
Tests various security vulnerabilities and fixes
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000/api"

def test_security():
    print("🔒 Testing Security Vulnerabilities")
    print("=" * 50)
    
    # Test 1: SQL Injection Attempt
    print("\n1️⃣ Testing SQL Injection Protection...")
    malicious_data = {
        "username": "admin'; DROP TABLE auth_user; --",
        "email": "test@example.com",
        "name": "Test User",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=malicious_data)
        if response.status_code == 400:
            print("✅ SQL Injection protection working!")
        else:
            print(f"❌ Potential SQL injection vulnerability: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing SQL injection: {e}")
    
    # Test 2: XSS Protection
    print("\n2️⃣ Testing XSS Protection...")
    xss_data = {
        "first_name": "<script>alert('XSS')</script>",
        "last_name": "Doe",
        "email": "xss@example.com",
        "date_of_birth": "1990-01-01",
        "phone": "1234567890"
    }
    
    try:
        # First register a user
        user_data = {
            "username": "testuser2",
            "email": "test2@example.com",
            "name": "Test User 2",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
        
        reg_response = requests.post(f"{BASE_URL}/auth/register/", json=user_data)
        if reg_response.status_code == 201:
            access_token = reg_response.json()['tokens']['access']
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Try to create patient with XSS payload
            response = requests.post(f"{BASE_URL}/patients/", json=xss_data, headers=headers)
            if response.status_code == 201:
                patient_data = response.json()
                if "<script>" not in patient_data['first_name']:
                    print("✅ XSS protection working!")
                else:
                    print("❌ XSS vulnerability detected!")
            else:
                print(f"❌ Patient creation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing XSS: {e}")
    
    # Test 3: Rate Limiting
    print("\n3️⃣ Testing Rate Limiting...")
    login_data = {"username": "nonexistent", "password": "wrongpassword"}
    
    try:
        for i in range(12):  # Try 12 times (limit is 10)
            response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
            if response.status_code == 429:
                print(f"✅ Rate limiting working! Blocked after {i+1} attempts")
                break
            elif i == 11:
                print("❌ Rate limiting not working properly")
    except Exception as e:
        print(f"❌ Error testing rate limiting: {e}")
    
    # Test 4: Authentication Bypass
    print("\n4️⃣ Testing Authentication Bypass...")
    try:
        # Try to access protected endpoint without token
        response = requests.get(f"{BASE_URL}/patients/")
        if response.status_code == 401:
            print("✅ Authentication required - no bypass possible!")
        else:
            print(f"❌ Authentication bypass possible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing auth bypass: {e}")
    
    # Test 5: Data Validation
    print("\n5️⃣ Testing Input Validation...")
    invalid_data = {
        "first_name": "",  # Empty name
        "last_name": "Doe",
        "email": "invalid-email",  # Invalid email
        "phone": "123",  # Too short phone
    }
    
    try:
        # Register user first
        user_data = {
            "username": "testuser3",
            "email": "test3@example.com",
            "name": "Test User 3",
            "password": "testpass123",
            "password_confirm": "testpass123"
        }
        
        reg_response = requests.post(f"{BASE_URL}/auth/register/", json=user_data)
        if reg_response.status_code == 201:
            access_token = reg_response.json()['tokens']['access']
            headers = {"Authorization": f"Bearer {access_token}"}
            
            response = requests.post(f"{BASE_URL}/patients/", json=invalid_data, headers=headers)
            if response.status_code == 400:
                print("✅ Input validation working!")
                errors = response.json()
                print(f"   Validation errors: {list(errors.keys())}")
            else:
                print(f"❌ Input validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing validation: {e}")
    
    # Test 6: Password Confirmation
    print("\n6️⃣ Testing Password Confirmation...")
    password_mismatch_data = {
        "username": "testuser4",
        "email": "test4@example.com",
        "name": "Test User 4",
        "password": "testpass123",
        "password_confirm": "differentpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=password_mismatch_data)
        if response.status_code == 400:
            print("✅ Password confirmation validation working!")
        else:
            print(f"❌ Password confirmation validation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing password confirmation: {e}")
    
    print("\n" + "=" * 50)
    print("🔒 Security Testing Complete!")

if __name__ == "__main__":
    test_security()
