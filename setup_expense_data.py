"""
Setup sample expense data for Madrasha accounting
"""
from app import create_app
from models import db, Expense
from datetime import date
from decimal import Decimal

app = create_app()

with app.app_context():
    try:
        # Check if expenses already exist
        existing = Expense.query.first()
        if existing:
            print('✅ Expense data already exists!')
        else:
            # Sample expenses for January 2025
            expenses = [
                {
                    'category': 'salary',
                    'description': 'উস্তাদ মাসিক বেতন - জানুয়ারি ২০২৫',
                    'amount': Decimal('15000.00'),
                    'date': date(2025, 1, 31),
                    'recipient': 'উস্তাদ আব্দুল্লাহ',
                    'payment_method': 'Cash',
                    'notes': 'প্রধান উস্তাদ মাসিক বেতন'
                },
                {
                    'category': 'salary',
                    'description': 'সহকারী উস্তাদ বেতন - জানুয়ারি',
                    'amount': Decimal('10000.00'),
                    'date': date(2025, 1, 31),
                    'recipient': 'উস্তাদ মুহাম্মদ',
                    'payment_method': 'Bank Transfer',
                    'notes': 'সহকারী উস্তাদ মাসিক বেতন'
                },
                {
                    'category': 'books',
                    'description': 'কুরআন শিক্ষার বই ক্রয়',
                    'amount': Decimal('3500.00'),
                    'date': date(2025, 1, 15),
                    'recipient': 'ইসলামিক বুক ডিপো',
                    'payment_method': 'Cash',
                    'notes': 'নতুন শিক্ষার্থীদের জন্য ২০টি কুরআন বই'
                },
                {
                    'category': 'books',
                    'description': 'আরবি ব্যাকরণ বই',
                    'amount': Decimal('2000.00'),
                    'date': date(2025, 1, 10),
                    'recipient': 'মক্তব বুক স্টোর',
                    'payment_method': 'Cash',
                    'notes': '১ম ও ২য় শ্রেণীর জন্য'
                },
                {
                    'category': 'utilities',
                    'description': 'বিদ্যুৎ বিল - জানুয়ারি',
                    'amount': Decimal('1200.00'),
                    'date': date(2025, 1, 20),
                    'recipient': 'DESCO',
                    'payment_method': 'Online Payment',
                    'notes': 'মাদ্রাসা ভবন বিদ্যুৎ বিল'
                },
                {
                    'category': 'stationery',
                    'description': 'খাতা, কলম ও স্টেশনারি',
                    'amount': Decimal('1500.00'),
                    'date': date(2025, 1, 5),
                    'recipient': 'স্টেশনারি মার্ট',
                    'payment_method': 'Cash',
                    'notes': 'সকল ক্লাসের জন্য'
                },
                {
                    'category': 'maintenance',
                    'description': 'ক্লাসরুম মেরামত',
                    'amount': Decimal('5000.00'),
                    'date': date(2025, 1, 12),
                    'recipient': 'করিম কন্সট্রাকশন',
                    'payment_method': 'Cash',
                    'notes': 'দেয়াল রং ও পাখা মেরামত'
                },
                {
                    'category': 'instruments',
                    'description': 'হোয়াইটবোর্ড ও মার্কার ক্রয়',
                    'amount': Decimal('2500.00'),
                    'date': date(2025, 1, 8),
                    'recipient': 'অফিস ইকুইপমেন্ট',
                    'payment_method': 'Cash',
                    'notes': 'তিনটি নতুন ক্লাসরুমের জন্য'
                },
                {
                    'category': 'rent',
                    'description': 'মাদ্রাসা ভবন ভাড়া - জানুয়ারি',
                    'amount': Decimal('12000.00'),
                    'date': date(2025, 1, 1),
                    'recipient': 'মালিক সাহেব',
                    'payment_method': 'Bank Transfer',
                    'notes': 'মাসিক ভাড়া'
                },
                {
                    'category': 'events',
                    'description': 'কুরআন তিলাওয়াত প্রতিযোগিতা আয়োজন',
                    'amount': Decimal('3000.00'),
                    'date': date(2025, 1, 25),
                    'recipient': 'বিভিন্ন',
                    'payment_method': 'Cash',
                    'notes': 'পুরস্কার ও রিফ্রেশমেন্ট'
                }
            ]
            
            for exp_data in expenses:
                expense = Expense(**exp_data)
                db.session.add(expense)
            
            db.session.commit()
            print('✅ Sample expense data created successfully!')
            
            # Calculate totals
            total = sum(Decimal(str(exp['amount'])) for exp in expenses)
            print(f'\n📊 Total Expenses Added: ৳{total:,.2f}')
            
            print('\n💰 Expenses by Category:')
            by_category = {}
            for exp in expenses:
                cat = exp['category']
                if cat not in by_category:
                    by_category[cat] = Decimal('0')
                by_category[cat] += exp['amount']
            
            for cat, amount in by_category.items():
                print(f'   - {cat}: ৳{amount:,.2f}')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        import traceback
        traceback.print_exc()
