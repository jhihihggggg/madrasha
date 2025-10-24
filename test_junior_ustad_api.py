"""
Test Junior Ustad API and Login Flow
"""
import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("🧪 TESTING JUNIOR USTAD SYSTEM")
print("=" * 60)

# Test 1: Junior Ustad Login
print("\n1️⃣ Testing Junior Ustad Login...")
login_data = {
    "phoneNumber": "01999999999",
    "password": "junior123"
}

response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    if data['success']:
        print("✅ Login successful!")
        print(f"   User: {data['data']['user']['name']}")
        print(f"   Role: {data['data']['user']['role']}")
        print(f"   Phone: {data['data']['user']['phoneNumber']}")
        session_cookie = response.cookies.get('session')
        print(f"   Session: {session_cookie[:20] if session_cookie else 'None'}...")
    else:
        print(f"❌ Login failed: {data.get('error', 'Unknown error')}")
else:
    print(f"❌ HTTP Error: {response.status_code}")
    print(f"   Response: {response.text[:200]}")

# Test 2: Admin Login
print("\n2️⃣ Testing Admin Login...")
admin_login_data = {
    "phoneNumber": "01712345678",
    "password": "admin123"
}

admin_response = requests.post(f"{BASE_URL}/api/auth/login", json=admin_login_data)
print(f"Status: {admin_response.status_code}")

if admin_response.status_code == 200:
    admin_data = admin_response.json()
    if admin_data['success']:
        print("✅ Admin login successful!")
        print(f"   User: {admin_data['data']['user']['name']}")
        print(f"   Role: {admin_data['data']['user']['role']}")
        
        # Test 3: Get Junior Ustads (requires admin session)
        print("\n3️⃣ Testing Get Junior Ustads API (with admin session)...")
        session = requests.Session()
        session.cookies = admin_response.cookies
        
        jr_response = session.get(f"{BASE_URL}/api/junior-ustad/")
        print(f"Status: {jr_response.status_code}")
        
        if jr_response.status_code == 200:
            jr_data = jr_response.json()
            if jr_data['success']:
                print("✅ API works!")
                print(f"   Found {len(jr_data['data']['junior_ustads'])} junior ustads")
                for ju in jr_data['data']['junior_ustads']:
                    print(f"   - {ju['name']} ({ju['phone']})")
            else:
                print(f"❌ API error: {jr_data.get('error', 'Unknown')}")
        else:
            print(f"❌ HTTP Error: {jr_response.status_code}")
            print(f"   Response: {jr_response.text[:200]}")
        
        # Test 4: Create New Junior Ustad
        print("\n4️⃣ Testing Create Junior Ustad API...")
        new_ju_data = {
            "first_name": "মোহাম্মদ",
            "last_name": "আলী",
            "phone": "01888888888",
            "password": "test123",
            "email": "mohammad@madrasha.com"
        }
        
        create_response = session.post(f"{BASE_URL}/api/junior-ustad/", json=new_ju_data)
        print(f"Status: {create_response.status_code}")
        
        if create_response.status_code in [200, 201]:
            create_data = create_response.json()
            if create_data['success']:
                print("✅ Junior Ustad created successfully!")
                print(f"   Name: {create_data['data']['name']}")
                print(f"   Phone: {create_data['data']['phone']}")
                new_ju_id = create_data['data']['id']
                
                # Test 5: Login with new junior ustad
                print("\n5️⃣ Testing Login with New Junior Ustad...")
                new_ju_login = {
                    "phoneNumber": "01888888888",
                    "password": "test123"
                }
                new_ju_response = requests.post(f"{BASE_URL}/api/auth/login", json=new_ju_login)
                if new_ju_response.status_code == 200:
                    new_ju_login_data = new_ju_response.json()
                    if new_ju_login_data['success']:
                        print("✅ New junior ustad login successful!")
                        print(f"   User: {new_ju_login_data['data']['user']['name']}")
                    else:
                        print(f"❌ Login failed: {new_ju_login_data.get('error')}")
                else:
                    print(f"❌ HTTP Error: {new_ju_response.status_code}")
                
            else:
                print(f"⚠️  Create failed: {create_data.get('error', 'Unknown')}")
        else:
            print(f"❌ HTTP Error: {create_response.status_code}")
            try:
                print(f"   Response: {create_response.json()}")
            except:
                print(f"   Response: {create_response.text[:200]}")

print("\n" + "=" * 60)
print("✅ TESTING COMPLETE!")
print("=" * 60)
print("\n💡 Access the system:")
print(f"   🏠 Homepage: {BASE_URL}/")
print(f"   🔐 Login: {BASE_URL}/login")
print(f"   ⚙️  Junior Ustad Management: {BASE_URL}/junior-ustad-management")
print()
