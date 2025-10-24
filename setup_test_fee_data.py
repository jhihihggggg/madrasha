"""
Setup test data for fee management system
"""
from app import create_app
from models import db, User, Batch, UserRole, Fee, FeeStatus
from datetime import datetime, date
from decimal import Decimal
import calendar

app = create_app()

with app.app_context():
    try:
        # Check if we already have batches
        existing_batch = Batch.query.first()
        if existing_batch:
            print('✅ Test data already exists!')
            print(f'   Found batch: {existing_batch.name}')
        else:
            # Create test batches
            batch1 = Batch(
                name='HSC 2025 - Physics',
                description='HSC Physics preparation batch',
                fee_amount=Decimal('1500.00'),
                start_date=date(2025, 1, 1),
                is_active=True
            )
            db.session.add(batch1)
            
            batch2 = Batch(
                name='HSC 2025 - Chemistry',
                description='HSC Chemistry preparation batch',
                fee_amount=Decimal('1200.00'),
                start_date=date(2025, 1, 1),
                is_active=True
            )
            db.session.add(batch2)
            
            db.session.commit()
            print('✅ Test batches created!')
            
            # Get student user
            student = User.query.filter_by(phoneNumber='01912345678').first()
            
            if student:
                # Enroll student in batch1
                student.batches.append(batch1)
                db.session.commit()
                print(f'✅ Student enrolled in {batch1.name}')
                
                # Create some sample fees for the student
                # January fee
                jan_fee = Fee(
                    user_id=student.id,
                    batch_id=batch1.id,
                    amount=Decimal('1500.00'),
                    due_date=date(2025, 1, 31),
                    status=FeeStatus.PAID,
                    paid_date=date(2025, 1, 15),
                    payment_method='Cash',
                    notes='Monthly fee for January 2025'
                )
                db.session.add(jan_fee)
                
                # February fee (pending)
                feb_fee = Fee(
                    user_id=student.id,
                    batch_id=batch1.id,
                    amount=Decimal('1500.00'),
                    due_date=date(2025, 2, 28),
                    status=FeeStatus.PENDING,
                    notes='Monthly fee for February 2025'
                )
                db.session.add(feb_fee)
                
                # March fee (overdue)
                mar_fee = Fee(
                    user_id=student.id,
                    batch_id=batch1.id,
                    amount=Decimal('1500.00'),
                    due_date=date(2025, 3, 31),
                    status=FeeStatus.OVERDUE,
                    late_fee=Decimal('100.00'),
                    notes='Monthly fee for March 2025'
                )
                db.session.add(mar_fee)
                
                db.session.commit()
                print('✅ Sample fees created for student!')
                print('   - January: Paid')
                print('   - February: Pending')
                print('   - March: Overdue (with late fee)')
            
        # Print summary
        print('\n📊 Current Database Summary:')
        print(f'   Total Users: {User.query.count()}')
        print(f'   Total Batches: {Batch.query.count()}')
        print(f'   Total Fees: {Fee.query.count()}')
        print(f'   Pending Fees: {Fee.query.filter_by(status=FeeStatus.PENDING).count()}')
        print(f'   Paid Fees: {Fee.query.filter_by(status=FeeStatus.PAID).count()}')
        print(f'   Overdue Fees: {Fee.query.filter_by(status=FeeStatus.OVERDUE).count()}')
        
    except Exception as e:
        print(f'❌ Error setting up test data: {e}')
        import traceback
        traceback.print_exc()
