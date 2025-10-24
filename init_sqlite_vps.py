#!/usr/bin/env python3
"""
Initialize SQLite database for VPS deployment
Creates database file and default users
"""
import os
import sys

# Get the absolute path to the project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)

# Ensure we're using SQLite with ABSOLUTE path
db_path = os.path.join(PROJECT_DIR, 'instance', 'madrasha.db')
os.environ['DATABASE_URL'] = f'sqlite:///{db_path}'
os.environ['FLASK_ENV'] = 'production'

# Remove any MySQL environment variables
for key in ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']:
    os.environ.pop(key, None)

print("🗄️  Initializing SQLite database...")
print(f"   Working directory: {os.getcwd()}")
print(f"   Database path: {db_path}")

from app import create_app
from models import db, User, UserRole
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    try:
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Check if users already exist
        existing_count = User.query.count()
        if existing_count > 0:
            print(f"ℹ️  Database already has {existing_count} users")
            sys.exit(0)
        
        print("👥 Creating default users...")
        
        # Create admin
        admin = User(
            phoneNumber='01712345678',
            first_name='Admin',
            last_name='User',
            role=UserRole.SUPER_USER,
            password_hash=generate_password_hash('admin123'),
            is_active=True,
            email='admin@madrasaummulqura.com'
        )
        db.session.add(admin)
        print("   ✓ Admin user created")
        
        # Create teacher
        teacher = User(
            phoneNumber='01812345678',
            first_name='Sample',
            last_name='Teacher',
            role=UserRole.TEACHER,
            password_hash=generate_password_hash('teacher123'),
            is_active=True,
            email='teacher@madrasaummulqura.com'
        )
        db.session.add(teacher)
        print("   ✓ Teacher user created")
        
        # Create student
        student = User(
            phoneNumber='01912345678',
            first_name='Sample',
            last_name='Student',
            role=UserRole.STUDENT,
            password_hash=generate_password_hash('student123'),
            is_active=True,
            guardian_phone='01712345670'
        )
        db.session.add(student)
        print("   ✓ Student user created")
        
        # Create junior ustad
        junior = User(
            phoneNumber='01999999999',
            first_name='Junior',
            last_name='Ustad',
            role=UserRole.JUNIOR_USTADH,
            password_hash=generate_password_hash('junior123'),
            is_active=True,
            email='junior@madrasaummulqura.com'
        )
        db.session.add(junior)
        print("   ✓ Junior Ustad user created")
        
        db.session.commit()
        
        print("\n✅ Database initialized successfully!")
        print(f"   Total users created: {User.query.count()}")
        print("\n📱 Default Credentials:")
        print("   Admin:   01712345678 / admin123")
        print("   Teacher: 01812345678 / teacher123")
        print("   Student: 01912345678 / student123")
        print("   Junior:  01999999999 / junior123")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
