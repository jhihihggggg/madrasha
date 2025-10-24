"""
Madrasha Accounting Routes - আয়-ব্যয় হিসাব-নিকাশ
Income and Expense Management System
"""
from flask import Blueprint, request, jsonify, session
from models import db, User, UserRole
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import extract, func
import calendar

accounting_bp = Blueprint('accounting', __name__)

def success_response(message, data=None, status=200):
    """Standard success response"""
    return jsonify({
        'success': True,
        'message': message,
        'data': data
    }), status

def error_response(message, status=400):
    """Standard error response"""
    return jsonify({
        'success': False,
        'error': message
    }), status


@accounting_bp.route('/income-summary', methods=['GET'])
def income_summary():
    """
    Get income summary (from student fees)
    GET /api/accounting/income-summary?year=2025&month=1
    """
    try:
        year = request.args.get('year', type=int, default=datetime.now().year)
        month = request.args.get('month', type=int)
        
        from models import Fee, FeeStatus
        
        query = Fee.query
        
        # Filter by year
        query = query.filter(extract('year', Fee.due_date) == year)
        
        # Filter by month if provided
        if month:
            query = query.filter(extract('month', Fee.due_date) == month)
        
        # Get all fees
        all_fees = query.all()
        
        # Calculate totals
        total_expected = sum(float(fee.amount) for fee in all_fees)
        total_paid = sum(float(fee.amount) for fee in all_fees if fee.status == FeeStatus.PAID)
        total_pending = sum(float(fee.amount) for fee in all_fees if fee.status == FeeStatus.PENDING)
        total_overdue = sum(float(fee.amount) for fee in all_fees if fee.status == FeeStatus.OVERDUE)
        
        return success_response('Income summary retrieved', {
            'year': year,
            'month': month,
            'total_expected': total_expected,
            'total_paid': total_paid,
            'total_pending': total_pending,
            'total_overdue': total_overdue,
            'collection_rate': round((total_paid / total_expected * 100) if total_expected > 0 else 0, 2)
        })
        
    except Exception as e:
        return error_response(f'Failed to get income summary: {str(e)}', 500)


@accounting_bp.route('/expenses', methods=['GET'])
def get_expenses():
    """
    Get all expenses
    GET /api/accounting/expenses?year=2025&month=1&category=salary
    """
    try:
        from models import Expense
        
        year = request.args.get('year', type=int)
        month = request.args.get('month', type=int)
        category = request.args.get('category')
        
        query = Expense.query
        
        if year:
            query = query.filter(extract('year', Expense.date) == year)
        if month:
            query = query.filter(extract('month', Expense.date) == month)
        if category:
            query = query.filter(Expense.category == category)
        
        expenses = query.order_by(Expense.date.desc()).all()
        
        result = [{
            'id': exp.id,
            'category': exp.category,
            'description': exp.description,
            'amount': float(exp.amount),
            'date': exp.date.isoformat(),
            'payment_method': exp.payment_method,
            'recipient': exp.recipient,
            'notes': exp.notes,
            'created_by': exp.created_by
        } for exp in expenses]
        
        total = sum(float(exp.amount) for exp in expenses)
        
        return success_response('Expenses retrieved', {
            'expenses': result,
            'total': total,
            'count': len(expenses)
        })
        
    except Exception as e:
        return error_response(f'Failed to get expenses: {str(e)}', 500)


@accounting_bp.route('/expenses', methods=['POST'])
def add_expense():
    """
    Add new expense
    POST /api/accounting/expenses
    {
        "category": "salary",
        "description": "উস্তাদ বেতন - জানুয়ারি",
        "amount": 10000,
        "date": "2025-01-31",
        "recipient": "উস্তাদ নাম",
        "payment_method": "Cash",
        "notes": "মাসিক বেতন"
    }
    """
    try:
        from models import Expense
        
        data = request.get_json()
        
        # Validate required fields
        required = ['category', 'description', 'amount', 'date']
        for field in required:
            if field not in data:
                return error_response(f'{field} is required', 400)
        
        # Create expense
        expense = Expense(
            category=data['category'],
            description=data['description'],
            amount=Decimal(str(data['amount'])),
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            recipient=data.get('recipient'),
            payment_method=data.get('payment_method', 'Cash'),
            notes=data.get('notes'),
            created_by=session.get('user', {}).get('id')
        )
        
        db.session.add(expense)
        db.session.commit()
        
        return success_response('Expense added successfully', {
            'id': expense.id,
            'category': expense.category,
            'amount': float(expense.amount),
            'date': expense.date.isoformat()
        }, 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to add expense: {str(e)}', 500)


@accounting_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    """Update an expense"""
    try:
        from models import Expense
        
        expense = Expense.query.get(expense_id)
        if not expense:
            return error_response('Expense not found', 404)
        
        data = request.get_json()
        
        if 'category' in data:
            expense.category = data['category']
        if 'description' in data:
            expense.description = data['description']
        if 'amount' in data:
            expense.amount = Decimal(str(data['amount']))
        if 'date' in data:
            expense.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'recipient' in data:
            expense.recipient = data['recipient']
        if 'payment_method' in data:
            expense.payment_method = data['payment_method']
        if 'notes' in data:
            expense.notes = data['notes']
        
        expense.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response('Expense updated successfully')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to update expense: {str(e)}', 500)


@accounting_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    """Delete an expense"""
    try:
        from models import Expense
        
        expense = Expense.query.get(expense_id)
        if not expense:
            return error_response('Expense not found', 404)
        
        db.session.delete(expense)
        db.session.commit()
        
        return success_response('Expense deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Failed to delete expense: {str(e)}', 500)


@accounting_bp.route('/summary', methods=['GET'])
def accounting_summary():
    """
    Get complete accounting summary
    GET /api/accounting/summary?year=2025&month=1
    """
    try:
        from models import Fee, FeeStatus, Expense
        
        year = request.args.get('year', type=int, default=datetime.now().year)
        month = request.args.get('month', type=int)
        
        # Income from fees
        fee_query = Fee.query.filter(extract('year', Fee.due_date) == year)
        if month:
            fee_query = fee_query.filter(extract('month', Fee.due_date) == month)
        
        fees = fee_query.all()
        total_income = sum(float(fee.amount) for fee in fees if fee.status == FeeStatus.PAID)
        
        # Expenses
        expense_query = Expense.query.filter(extract('year', Expense.date) == year)
        if month:
            expense_query = expense_query.filter(extract('month', Expense.date) == month)
        
        expenses = expense_query.all()
        
        # Group expenses by category
        expenses_by_category = {}
        for exp in expenses:
            if exp.category not in expenses_by_category:
                expenses_by_category[exp.category] = 0
            expenses_by_category[exp.category] += float(exp.amount)
        
        total_expenses = sum(expenses_by_category.values())
        net_balance = total_income - total_expenses
        
        return success_response('Accounting summary retrieved', {
            'year': year,
            'month': month,
            'income': {
                'total': total_income,
                'from_fees': total_income
            },
            'expenses': {
                'total': total_expenses,
                'by_category': expenses_by_category
            },
            'balance': net_balance,
            'period': f'{calendar.month_name[month]} {year}' if month else str(year)
        })
        
    except Exception as e:
        return error_response(f'Failed to get accounting summary: {str(e)}', 500)


@accounting_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get expense categories"""
    categories = [
        {'value': 'salary', 'label': 'উস্তাদ বেতন', 'label_en': 'Teacher Salary'},
        {'value': 'books', 'label': 'বই ও পুস্তক', 'label_en': 'Books'},
        {'value': 'instruments', 'label': 'যন্ত্রপাতি', 'label_en': 'Instruments/Equipment'},
        {'value': 'utilities', 'label': 'ইউটিলিটি (বিদ্যুৎ, পানি)', 'label_en': 'Utilities'},
        {'value': 'rent', 'label': 'ভাড়া', 'label_en': 'Rent'},
        {'value': 'maintenance', 'label': 'রক্ষণাবেক্ষণ', 'label_en': 'Maintenance'},
        {'value': 'stationery', 'label': 'স্টেশনারি', 'label_en': 'Stationery'},
        {'value': 'transport', 'label': 'পরিবহন', 'label_en': 'Transport'},
        {'value': 'food', 'label': 'খাবার', 'label_en': 'Food'},
        {'value': 'events', 'label': 'অনুষ্ঠান', 'label_en': 'Events'},
        {'value': 'other', 'label': 'অন্যান্য', 'label_en': 'Other'}
    ]
    
    return success_response('Categories retrieved', {'categories': categories})
