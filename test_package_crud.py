#!/usr/bin/env python3

import subprocess
import json
import uuid

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

def test_package_crud():
    base_url = "http://localhost:8000"
    
    print("Getting auth token...")
    login_cmd = f'curl -s -X POST "{base_url}/auth/login" -H "Content-Type: application/json" -d \'{{"email": "admin@test.com", "password": "admin123"}}\''
    login_response = run_curl(login_cmd)
    
    if not login_response or "access_token" not in login_response:
        print("Failed to get auth token")
        return
    
    token = login_response["access_token"]
    headers = f'-H "Authorization: Bearer {token}" -H "Content-Type: application/json"'
    
    print("\nCreating test countries...")
    country_data = '{"iso_code": "LK", "name": "Sri Lanka"}'
    country_cmd = f'curl -s -X POST "{base_url}/admin/countries" {headers} -d \'{country_data}\''
    country_response = run_curl(country_cmd)
    print(f"Country created: {country_response}")
    
    if not country_response or "id" not in country_response:
        print("Failed to create country")
        return
    
    country_id = country_response["id"]
    
    print("\nCreating test warehouse...")
    warehouse_data = f'{{"name": "Colombo Warehouse", "city": "Colombo", "country_id": "{country_id}"}}'
    warehouse_cmd = f'curl -s -X POST "{base_url}/admin/warehouses" {headers} -d \'{warehouse_data}\''
    warehouse_response = run_curl(warehouse_cmd)
    print(f"Warehouse created: {warehouse_response}")
    
    if not warehouse_response or "id" not in warehouse_response:
        print("Failed to create warehouse")
        return
    
    warehouse_id = warehouse_response["id"]
    
    print("\nCreating test box type...")
    boxtype_data = '{"code": "SMALL", "dim_label": "Small Box (30x20x15cm)", "price_lkr": 500.00}'
    boxtype_cmd = f'curl -s -X POST "{base_url}/admin/boxtypes" {headers} -d \'{boxtype_data}\''
    boxtype_response = run_curl(boxtype_cmd)
    print(f"Box type created: {boxtype_response}")
    
    if not boxtype_response or "id" not in boxtype_response:
        print("Failed to create box type")
        return
    
    boxtype_id = boxtype_response["id"]
    
    print("\n=== Testing Package CRUD ===")
    
    print("\n1. Creating package...")
    package_data = f'''{{
        "sender_name": "John Doe",
        "sender_phone": "+94771234567",
        "receiver_name": "Jane Smith", 
        "receiver_phone": "+94779876543",
        "origin_wh_id": "{warehouse_id}",
        "dest_wh_id": "{warehouse_id}",
        "box_type_id": "{boxtype_id}"
    }}'''
    
    create_cmd = f'curl -s -X POST "{base_url}/packages/" {headers} -d \'{package_data}\''
    create_response = run_curl(create_cmd)
    print(f"Package created: {create_response}")
    
    if not create_response or "tracking_id" not in create_response:
        print("Failed to create package")
        return
    
    tracking_id = create_response["tracking_id"]
    
    print(f"\n2. Getting package by tracking ID: {tracking_id}")
    get_cmd = f'curl -s -X GET "{base_url}/packages/{tracking_id}" {headers}'
    get_response = run_curl(get_cmd)
    print(f"Package retrieved: {get_response}")
    
    print(f"\n3. Updating package status to IN_TRANSIT...")
    status_data = '{"status": "IN_TRANSIT"}'
    update_cmd = f'curl -s -X PATCH "{base_url}/packages/{tracking_id}/status" {headers} -d \'{status_data}\''
    update_response = run_curl(update_cmd)
    print(f"Status updated: {update_response}")
    
    print(f"\n4. Listing all packages...")
    list_cmd = f'curl -s -X GET "{base_url}/packages/" {headers}'
    list_response = run_curl(list_cmd)
    print(f"Package list: {list_response}")
    
    print("\n=== Package CRUD Test Complete ===")

if __name__ == "__main__":
    test_package_crud()
