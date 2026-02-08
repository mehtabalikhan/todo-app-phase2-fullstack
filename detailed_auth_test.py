#!/usr/bin/env python3
"""
Detailed test to verify authentication functionality on port 8001
"""

import requests
import json

def test_auth_flow():
    base_url = "http://127.0.0.1:8001"

    print("Testing authentication flow on port 8001...")

    # First, try to register a new user
    print("\n1. Testing registration...")
    register_data = {
        "email": "testuser@example.com",
        "password": "shortpass123",
        "name": "Test User"
    }

    try:
        response = requests.post(f"{base_url}/api/v1/register", json=register_data)
        print(f"Registration response: {response.status_code}")
        print(f"Registration response body: {response.text}")
        if response.status_code == 200:
            print("[SUCCESS] Registration successful!")
            response_data = response.json()
            print(f"  Access token received: {bool(response_data.get('access_token'))}")
            print(f"  Token type: {response_data.get('token_type')}")
            token = response_data.get('access_token')
        elif response.status_code == 409:
            print("[INFO] User already exists (this is fine for testing)")
            token = None
        elif response.status_code == 422:
            print(f"[ERROR] Validation error: {response.json()}")
        else:
            print(f"[ERROR] Registration failed: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Registration exception: {e}")
        token = None

    # Then, try to login with the user
    print("\n2. Testing login...")
    login_data = {
        "email": "testuser@example.com",
        "password": "shortpass123"
    }

    try:
        response = requests.post(f"{base_url}/api/v1/login", json=login_data)
        print(f"Login response: {response.status_code}")
        print(f"Login response body: {response.text}")
        if response.status_code == 200:
            print("[SUCCESS] Login successful!")
            response_data = response.json()
            print(f"  Access token received: {bool(response_data.get('access_token'))}")
            print(f"  Token type: {response_data.get('token_type')}")
            print(f"  User ID in token: {response_data.get('access_token')[:50]}..." if response_data.get('access_token') else "No token")
        elif response.status_code == 401:
            print("[ERROR] Login failed: Invalid credentials")
        elif response.status_code == 422:
            print(f"[ERROR] Validation error: {response.json()}")
        else:
            print(f"[ERROR] Login failed: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Login exception: {e}")

    # Test the health endpoint to make sure the server is running properly
    print("\n3. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health response: {response.status_code}")
        print(f"Health response body: {response.text}")
        if response.status_code == 200:
            print("[SUCCESS] Health check passed!")
            print(f"  Response: {response.json()}")
        else:
            print(f"[ERROR] Health check failed: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Health check exception: {e}")

if __name__ == "__main__":
    test_auth_flow()