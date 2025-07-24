#!/usr/bin/env python3

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.core.sms_service import sms_service
from app.core.config import settings

async def test_sms_integration():
    """Test SMS integration with Infobip sandbox"""
    print("=== Testing SMS Integration (Milestone 5) ===\n")
    
    print("1. Testing basic SMS sending...")
    test_phone = settings.TEST_RECEIVER_PHONE
    test_message = "Hello from Cargo SMS Alert System! This is a test message."
    
    result = await sms_service.send_sms(
        to=test_phone,
        message=test_message
    )
    
    print(f"SMS Result: {result}")
    print(f"Success: {'messageId' in result}")
    
    print("\n2. Testing package alert SMS...")
    alert_result = await sms_service.send_package_alert(
        phone=test_phone,
        tracking_id="PKG12345678",
        status="registered",
        language="en"
    )
    
    print(f"Package Alert Result: {alert_result}")
    print(f"Success: {'messageId' in alert_result}")
    
    print("\n3. Testing multilingual SMS (Sinhala)...")
    sinhala_result = await sms_service.send_package_alert(
        phone=test_phone,
        tracking_id="PKG12345678",
        status="in_transit",
        language="si"
    )
    
    print(f"Sinhala SMS Result: {sinhala_result}")
    print(f"Success: {'messageId' in sinhala_result}")
    
    print("\n4. Testing multilingual SMS (Tamil)...")
    tamil_result = await sms_service.send_package_alert(
        phone=test_phone,
        tracking_id="PKG12345678",
        status="delivered",
        language="ta"
    )
    
    print(f"Tamil SMS Result: {tamil_result}")
    print(f"Success: {'messageId' in tamil_result}")
    
    print("\n=== SMS Integration Test Complete ===")
    
    all_tests = [result, alert_result, sinhala_result, tamil_result]
    successful_tests = sum(1 for test in all_tests if 'messageId' in test)
    
    print(f"\nSummary: {successful_tests}/{len(all_tests)} tests passed")
    
    if successful_tests == len(all_tests):
        print("✅ All SMS integration tests passed!")
        return True
    else:
        print("❌ Some SMS integration tests failed!")
        return False

async def test_status_workflow():
    """Test complete status update workflow with SMS"""
    print("\n=== Testing Status Update Workflow ===")
    
    tracking_id = "PKG87654321"
    phone_sender = settings.TEST_SENDER_PHONE
    phone_receiver = settings.TEST_RECEIVER_PHONE
    
    statuses = ["registered", "in_transit", "delivered"]
    
    for i, status in enumerate(statuses, 1):
        print(f"\n{i}. Testing status: {status}")
        
        sender_result = await sms_service.send_package_alert(
            phone=phone_sender,
            tracking_id=tracking_id,
            status=status,
            language="en"
        )
        
        receiver_result = await sms_service.send_package_alert(
            phone=phone_receiver,
            tracking_id=tracking_id,
            status=status,
            language="en"
        )
        
        print(f"  Sender SMS: {'✅' if 'messageId' in sender_result else '❌'}")
        print(f"  Receiver SMS: {'✅' if 'messageId' in receiver_result else '❌'}")
        
        await asyncio.sleep(1)
    
    print("\n✅ Status update workflow test complete!")

if __name__ == "__main__":
    async def main():
        print(f"SMS Sandbox Mode: {settings.SMS_SANDBOX_MODE}")
        print(f"Infobip API Key: {'Set' if settings.INFOBIP_API_KEY else 'Not Set'}")
        print(f"Test Phones: {settings.TEST_SENDER_PHONE} -> {settings.TEST_RECEIVER_PHONE}\n")
        
        sms_success = await test_sms_integration()
        
        await test_status_workflow()
        
        return sms_success
    
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
