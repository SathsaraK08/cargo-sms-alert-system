#!/usr/bin/env python3

import subprocess
import json

def run_curl(cmd):
    """Run curl command and return response"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"Error: {result.stderr}")
        return None
    try:
        return json.loads(result.stdout) if result.stdout.strip() else None
    except json.JSONDecodeError:
        print(f"Invalid JSON response: {result.stdout}")
        return None

def test_status_update():
    base_url = "http://localhost:8000"
    
    login_cmd = f'curl -s -X POST "{base_url}/auth/login" -H "Content-Type: application/json" -d \'{{"email": "admin@test.com", "password": "admin123"}}\''
    login_response = run_curl(login_cmd)
    
    if not login_response or "access_token" not in login_response:
        print("Failed to get auth token")
        return
    
    token = login_response["access_token"]
    headers = f'-H "Authorization: Bearer {token}" -H "Content-Type: application/json"'
    
    tracking_id = "PKG96C53FBA"  # From previous test
    
    print(f"Testing status update with correct enum case...")
    status_data = '{"status": "in_transit"}'
    update_cmd = f'curl -s -X PATCH "{base_url}/packages/{tracking_id}/status" {headers} -d \'{status_data}\''
    update_response = run_curl(update_cmd)
    print(f"Status update result: {update_response}")
    
    print(f"Testing status update to delivered...")
    status_data = '{"status": "delivered"}'
    update_cmd = f'curl -s -X PATCH "{base_url}/packages/{tracking_id}/status" {headers} -d \'{status_data}\''
    update_response = run_curl(update_cmd)
    print(f"Delivered status result: {update_response}")

if __name__ == "__main__":
    test_status_update()
