#!/usr/bin/env python3
"""
Quick test script to demonstrate the fee management system
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_health():
    print_section("Testing Server Health")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_fee_routes():
    print_section("Testing Fee Routes")
    response = requests.get(f"{BASE_URL}/api/fees/test")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

def test_load_fees():
    print_section("Loading Monthly Fees for Batch 1, Year 2025")
    response = requests.get(f"{BASE_URL}/api/fees/load-monthly", params={
        'batch_id': 1,
        'year': 2025
    })
    print(f"Status: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print(f"\n✅ Successfully loaded fees for {data['data']['student_count']} students")
        print(f"   Batch ID: {data['data']['batch_id']}")
        print(f"   Year: {data['data']['year']}")
        
        # Show first student's fees
        if data['data']['fees']:
            student = data['data']['fees'][0]
            print(f"\n📊 Sample Student: {student['student_name']}")
            print("   Monthly Fee Status:")
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            for i, month_name in enumerate(months, 1):
                month_data = student['months'][str(i)]
                if month_data['fee_id']:
                    status_icon = {
                        'paid': '✅',
                        'pending': '⏳',
                        'overdue': '⚠️'
                    }.get(month_data['status'], '❓')
                    
                    print(f"   {month_name}: {status_icon} {month_data['status'].upper()} - "
                          f"৳{month_data['amount']:.2f}")
    else:
        print(f"❌ Error: {data.get('error')}")

def test_save_fee():
    print_section("Creating a New Fee Entry")
    
    # Create April fee
    fee_data = {
        'student_id': 2,  # Updated student ID
        'batch_id': 1,
        'month': 4,
        'year': 2025,
        'amount': 1500
    }
    
    print(f"Creating fee: {json.dumps(fee_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/api/fees/save-monthly",
        json=fee_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nStatus: {response.status_code}")
    data = response.json()
    
    if data.get('success'):
        print(f"✅ {data['message']}")
        if 'data' in data:
            print(f"   Fee ID: {data['data'].get('fee_id')}")
            print(f"   Amount: ৳{data['data'].get('amount'):.2f}")
            print(f"   Status: {data['data'].get('status', 'N/A').upper()}")
    else:
        print(f"❌ Error: {data.get('error')}")

def main():
    print("\n" + "🏛️  MADRASHA FINANCIAL MANAGEMENT SYSTEM TEST".center(60))
    print("=" * 60)
    
    try:
        # Run tests
        test_health()
        test_fee_routes()
        test_load_fees()
        test_save_fee()
        
        # Final reload to show updated data
        print_section("Reloading Fees After Update")
        response = requests.get(f"{BASE_URL}/api/fees/load-monthly", params={
            'batch_id': 1,
            'year': 2025
        })
        
        if response.json().get('success'):
            student = response.json()['data']['fees'][0]
            print(f"Student: {student['student_name']}")
            print("\nUpdated Fee Status (showing only months with fees):")
            
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            for i, month_name in enumerate(months, 1):
                month_data = student['months'][str(i)]
                if month_data['fee_id']:
                    status_icon = {
                        'paid': '✅',
                        'pending': '⏳',
                        'overdue': '⚠️'
                    }.get(month_data['status'], '❓')
                    
                    print(f"   {month_name}: {status_icon} {month_data['status'].upper()} - "
                          f"৳{month_data['amount']:.2f}")
        
        print("\n" + "="*60)
        print("✅ All tests completed successfully!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the server.")
        print("   Make sure the Flask app is running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()
