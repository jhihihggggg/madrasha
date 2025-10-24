"""
Create a test Junior Ustad account for testing
"""
from app import create_app
from models import db, User, UserRole
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    # Check if junior ustad already exists
    existing = User.query.filter_by(phoneNumber='01999999999').first()
    if existing:
        print(f"❌ Junior Ustad with phone 01999999999 already exists: {existing.first_name} {existing.last_name}")
        print(f"   ID: {existing.id}, Role: {existing.role.value}")
    else:
        # Create new junior ustad
        junior_ustad = User(
            phoneNumber='01999999999',
            first_name='আব্দুর',
            last_name='রহমান',
            email='juniorustad@madrasha.com',
            password_hash=generate_password_hash('junior123'),
            role=UserRole.JUNIOR_USTADH,
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        db.session.add(junior_ustad)
        db.session.commit()
        
        print("✅ Test Junior Ustad account created successfully!")
        print(f"   Name: {junior_ustad.first_name} {junior_ustad.last_name}")
        print(f"   Phone: {junior_ustad.phoneNumber}")
        print(f"   Password: junior123")
        print(f"   Role: {junior_ustad.role.value}")
        print(f"   ID: {junior_ustad.id}")
    
    # List all junior ustads
    print("\n📋 All Junior Ustads in database:")
    all_junior_ustads = User.query.filter_by(role=UserRole.JUNIOR_USTADH, is_archived=False).all()
    for ju in all_junior_ustads:
        status = "✓ Active" if ju.is_active else "✗ Inactive"
        print(f"   {ju.id}. {ju.first_name} {ju.last_name} - {ju.phoneNumber} [{status}]")
    
    if not all_junior_ustads:
        print("   (No junior ustads found)")
