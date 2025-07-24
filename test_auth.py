#!/usr/bin/env python3

import requests
import json

def test_auth():
    base_url = "http://localhost:8000"
    
    login_data = {
        "username": "admin@test.com",
        "password": "admin123"
    }
    
    print("Testing login endpoint...")
    response = requests.post(
        f"{base_url}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        token_data = response.json()
        if token_data and "access_token" in token_data:
            token = token_data["access_token"]
            print(f"Token received: {token[:50]}...")
            
            print("\nTesting protected endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            protected_response = requests.get(f"{base_url}/admin/countries", headers=headers)
            print(f"Protected endpoint status: {protected_response.status_code}")
            print(f"Protected response: {protected_response.text}")
        else:
            print("No access_token in response")
    else:
        print("Login failed")

if __name__ == "__main__":
    test_auth()
