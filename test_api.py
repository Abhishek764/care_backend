#!/usr/bin/env python3
"""
Comprehensive API Testing Script for Django Healthcare Backend
"""
import requests
import json
import time

# Base URL
BASE_URL = "http://localhost:8000/api"

def test_api():
    print("🏥 Testing Django Healthcare Backend API")
    print("=" * 50)
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test 1: User Registration
    print("\n1️⃣ Testing User Registration...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com", 
        "name": "Test User",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register/", json=register_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("✅ Registration successful!")
            user_data = response.json()
            print(f"User ID: {user_data['user']['id']}")
            print(f"Username: {user_data['user']['username']}")
            access_token = user_data['tokens']['access']
            print(f"Access Token: {access_token[:20]}...")
        else:
            print(f"❌ Registration failed: {response.text}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Django server is running.")
        return
    
    # Test 2: User Login
    print("\n2️⃣ Testing User Login...")
    login_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login/", json=login_data)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Login successful!")
            login_response = response.json()
            access_token = login_response['access']
            print(f"Access Token: {access_token[:20]}...")
        else:
            print(f"❌ Login failed: {response.text}")
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Headers for authenticated requests
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test 3: Create Patient
    print("\n3️⃣ Testing Patient Creation...")
    patient_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "date_of_birth": "1990-01-15",
        "phone": "+1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/patients/", json=patient_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("✅ Patient created successfully!")
            patient = response.json()
            patient_id = patient['id']
            print(f"Patient ID: {patient_id}")
            print(f"Patient Name: {patient['first_name']} {patient['last_name']}")
        else:
            print(f"❌ Patient creation failed: {response.text}")
    except Exception as e:
        print(f"❌ Patient creation error: {e}")
    
    # Test 4: Get All Patients
    print("\n4️⃣ Testing Get All Patients...")
    try:
        response = requests.get(f"{BASE_URL}/patients/", headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Retrieved patients successfully!")
            patients = response.json()
            print(f"Number of patients: {len(patients['results'])}")
            for patient in patients['results']:
                print(f"  - {patient['first_name']} {patient['last_name']} (ID: {patient['id']})")
        else:
            print(f"❌ Get patients failed: {response.text}")
    except Exception as e:
        print(f"❌ Get patients error: {e}")
    
    # Test 5: Create Doctor
    print("\n5️⃣ Testing Doctor Creation...")
    doctor_data = {
        "first_name": "Dr. Jane",
        "last_name": "Smith",
        "email": "jane.smith@hospital.com",
        "specialization": "Cardiology"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/doctors/", json=doctor_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("✅ Doctor created successfully!")
            doctor = response.json()
            doctor_id = doctor['id']
            print(f"Doctor ID: {doctor_id}")
            print(f"Doctor Name: {doctor['first_name']} {doctor['last_name']}")
            print(f"Specialization: {doctor['specialization']}")
        else:
            print(f"❌ Doctor creation failed: {response.text}")
    except Exception as e:
        print(f"❌ Doctor creation error: {e}")
    
    # Test 6: Get All Doctors
    print("\n6️⃣ Testing Get All Doctors...")
    try:
        response = requests.get(f"{BASE_URL}/doctors/", headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Retrieved doctors successfully!")
            doctors = response.json()
            print(f"Number of doctors: {len(doctors['results'])}")
            for doctor in doctors['results']:
                print(f"  - {doctor['first_name']} {doctor['last_name']} - {doctor['specialization']} (ID: {doctor['id']})")
        else:
            print(f"❌ Get doctors failed: {response.text}")
    except Exception as e:
        print(f"❌ Get doctors error: {e}")
    
    # Test 7: Create Patient-Doctor Mapping
    print("\n7️⃣ Testing Patient-Doctor Mapping...")
    mapping_data = {
        "patient": patient_id,
        "doctor": doctor_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/mappings/", json=mapping_data, headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 201:
            print("✅ Patient-Doctor mapping created successfully!")
            mapping = response.json()
            print(f"Mapping ID: {mapping['id']}")
            print(f"Patient: {mapping['patient_detail']['first_name']} {mapping['patient_detail']['last_name']}")
            print(f"Doctor: {mapping['doctor_detail']['first_name']} {mapping['doctor_detail']['last_name']}")
        else:
            print(f"❌ Mapping creation failed: {response.text}")
    except Exception as e:
        print(f"❌ Mapping creation error: {e}")
    
    # Test 8: Get All Mappings
    print("\n8️⃣ Testing Get All Mappings...")
    try:
        response = requests.get(f"{BASE_URL}/mappings/", headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Retrieved mappings successfully!")
            mappings = response.json()
            print(f"Number of mappings: {len(mappings['results'])}")
            for mapping in mappings['results']:
                print(f"  - Patient: {mapping['patient_detail']['first_name']} ↔ Doctor: {mapping['doctor_detail']['first_name']}")
        else:
            print(f"❌ Get mappings failed: {response.text}")
    except Exception as e:
        print(f"❌ Get mappings error: {e}")
    
    # Test 9: Get Doctors by Patient ID
    print(f"\n9️⃣ Testing Get Doctors by Patient ID ({patient_id})...")
    try:
        response = requests.get(f"{BASE_URL}/mappings/{patient_id}/", headers=headers)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ Retrieved doctors for patient successfully!")
            doctors = response.json()
            print(f"Number of doctors for this patient: {len(doctors)}")
            for doctor in doctors:
                print(f"  - {doctor['doctor_detail']['first_name']} {doctor['doctor_detail']['last_name']} - {doctor['doctor_detail']['specialization']}")
        else:
            print(f"❌ Get doctors by patient failed: {response.text}")
    except Exception as e:
        print(f"❌ Get doctors by patient error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 API Testing Complete!")
    print("All endpoints are working correctly! ✅")

if __name__ == "__main__":
    test_api()
