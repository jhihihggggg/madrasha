"""
Test Junior Ustad Creation as Teacher
"""
import requests

BASE_URL = "http://localhost:5000"

# Login as teacher
print("🔐 Logging in as Teacher...")
login_data = {
    "phoneNumber": "01812345678",
    "password": "teacher123"
}

session = requests.Session()
response = session.post(f"{BASE_URL}/api/auth/login", json=login_data)

if response.status_code == 200:
    data = response.json()
    print(f"✅ Logged in as: {data['data']['user']['name']} ({data['data']['user']['role']})")
    
    # Try to get junior ustads
    print("\n📋 Getting junior ustads list...")
    jr_response = session.get(f"{BASE_URL}/api/junior-ustad/")
    print(f"Status: {jr_response.status_code}")
    
    if jr_response.status_code == 200:
        jr_data = jr_response.json()
        if jr_data['success']:
            print(f"✅ Found {len(jr_data['data']['junior_ustads'])} junior ustads")
        else:
            print(f"❌ Error: {jr_data.get('error')}")
    else:
        print(f"❌ HTTP Error: {jr_response.status_code}")
        print(f"Response: {jr_response.text}")
    
    # Try to create a junior ustad
    print("\n➕ Creating new junior ustad...")
    new_ju = {
        "first_name": "সাইফুল",
        "last_name": "ইসলাম",
        "phone": "01666666666",
        "password": "saiful123",
        "email": "saiful@madrasha.com"
    }
    
    create_response = session.post(f"{BASE_URL}/api/junior-ustad/", json=new_ju)
    print(f"Status: {create_response.status_code}")
    
    if create_response.status_code in [200, 201]:
        create_data = create_response.json()
        if create_data['success']:
            print(f"✅ Created: {create_data['data']['name']} ({create_data['data']['phone']})")
        else:
            print(f"⚠️ Error: {create_data.get('error')}")
    else:
        print(f"❌ HTTP Error: {create_response.status_code}")
        print(f"Response: {create_response.text[:200]}")
else:
    print(f"❌ Login failed: {response.status_code}")
