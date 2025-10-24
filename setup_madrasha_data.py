"""
Setup Madrasha test data with Islamic classes and subjects
"""
from app import create_app
from models import db, User, Batch, UserRole
from datetime import date
from decimal import Decimal

app = create_app()

with app.app_context():
    try:
        # Check if we already have batches
        existing_batch = Batch.query.first()
        if existing_batch:
            print('✅ Test data already exists!')
            print(f'   Found batch: {existing_batch.name}')
        else:
            # Create Madrasha classes
            batches = [
                {
                    'name': 'বেবি ক্লাস',
                    'description': 'আরবি ও বাংলা বর্ণমালা, মৌলিক দোয়া ও সুরা',
                    'fee_amount': Decimal('500.00'),
                    'start_date': date(2025, 1, 1)
                },
                {
                    'name': 'প্রথম শ্রেণী',
                    'description': 'কুরআন নাযেরা, বাংলা, গণিত, আকাইদ ও ফিকহ',
                    'fee_amount': Decimal('800.00'),
                    'start_date': date(2025, 1, 1)
                },
                {
                    'name': 'দ্বিতীয় শ্রেণী',
                    'description': 'কুরআন নাযেরা, বাংলা, ইংরেজি, গণিত, আরবি ব্যাকরণ',
                    'fee_amount': Decimal('900.00'),
                    'start_date': date(2025, 1, 1)
                },
                {
                    'name': 'তৃতীয় শ্রেণী',
                    'description': 'কুরআন তাজবীদসহ, বাংলা, ইংরেজি, গণিত, হাদীস ও ফিকহ',
                    'fee_amount': Decimal('1000.00'),
                    'start_date': date(2025, 1, 1)
                },
                {
                    'name': 'চতুর্থ শ্রেণী',
                    'description': 'কুরআন হিফজ শুরু, সকল সাধারণ বিষয়, আরবি সাহিত্য, ইসলামের ইতিহাস',
                    'fee_amount': Decimal('1200.00'),
                    'start_date': date(2025, 1, 1)
                },
                {
                    'name': 'পঞ্চম শ্রেণী',
                    'description': 'কুরআন হিফজ, বাংলা, ইংরেজি, গণিত, বিজ্ঞান, হাদীস ও সীরাহ',
                    'fee_amount': Decimal('1500.00'),
                    'start_date': date(2025, 1, 1)
                }
            ]
            
            for batch_data in batches:
                batch = Batch(
                    name=batch_data['name'],
                    description=batch_data['description'],
                    fee_amount=batch_data['fee_amount'],
                    start_date=batch_data['start_date'],
                    is_active=True
                )
                db.session.add(batch)
            
            db.session.commit()
            print('✅ Madrasha classes (batches) created successfully!')
            
            # Get student and enroll in a class
            student = User.query.filter_by(phoneNumber='01912345678').first()
            if student:
                batch = Batch.query.filter_by(name='তৃতীয় শ্রেণী').first()
                if batch:
                    student.batches.append(batch)
                    db.session.commit()
                    print(f'✅ Sample student enrolled in {batch.name}')
        
        # Print summary
        print('\n📊 Current Madrasha Database Summary:')
        print(f'   Total Users: {User.query.count()}')
        print(f'   - Students: {User.query.filter_by(role=UserRole.STUDENT).count()}')
        print(f'   - Ustadh/Teachers: {User.query.filter_by(role=UserRole.TEACHER).count()}')
        print(f'   - Admins: {User.query.filter_by(role=UserRole.SUPER_USER).count()}')
        print(f'   Total Classes (Batches): {Batch.query.count()}')
        
        print('\n📚 Classes:')
        for batch in Batch.query.all():
            print(f'   - {batch.name}: ৳{batch.fee_amount}/মাস')
        
    except Exception as e:
        print(f'❌ Error setting up test data: {e}')
        import traceback
        traceback.print_exc()
