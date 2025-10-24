"""
Junior Ustad (Assistant Teacher) Management Routes
Allows admin to create, edit, delete junior ustad accounts
"""
from flask import Blueprint, render_template, request, jsonify, session
from models import db, User, UserRole
from werkzeug.security import generate_password_hash
from datetime import datetime
from functools import wraps

junior_ustad_bp = Blueprint('junior_ustad', __name__)

def admin_required(f):
    """Decorator to require admin/super_user or senior teacher role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'অনুমতি নেই'}), 403
        
        user = User.query.get(session['user_id'])
        if not user or (user.role != UserRole.SUPER_USER and user.role != UserRole.TEACHER):
            return jsonify({'success': False, 'error': 'শুধুমাত্র প্রশাসক বা উস্তাদ এই কাজ করতে পারবেন'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@junior_ustad_bp.route('/', methods=['GET'])
@admin_required
def get_junior_ustads():
    """Get all junior ustad accounts"""
    try:
        junior_ustads = User.query.filter_by(
            role=UserRole.JUNIOR_USTADH,
            is_archived=False
        ).order_by(User.created_at.desc()).all()
        
        data = [{
            'id': ju.id,
            'name': f"{ju.first_name} {ju.last_name}",
            'phone': ju.phoneNumber,
            'email': ju.email,
            'is_active': ju.is_active,
            'created_at': ju.created_at.isoformat() if ju.created_at else None,
            'last_login': ju.last_login.isoformat() if ju.last_login else None
        } for ju in junior_ustads]
        
        return jsonify({
            'success': True,
            'data': {'junior_ustads': data},
            'message': f'{len(data)}টি জুনিয়র উস্তাদ পাওয়া গেছে'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@junior_ustad_bp.route('/', methods=['POST'])
@admin_required
def create_junior_ustad():
    """Create a new junior ustad account"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'phone', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'error': f'{field} প্রয়োজন'
                }), 400
        
        # Check if phone number already exists
        existing_user = User.query.filter_by(phoneNumber=data['phone']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'এই ফোন নম্বর ইতিমধ্যে ব্যবহৃত হয়েছে'
            }), 400
        
        # Create new junior ustad
        junior_ustad = User(
            phoneNumber=data['phone'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data.get('email'),
            password_hash=generate_password_hash(data['password']),
            role=UserRole.JUNIOR_USTADH,
            is_active=True,
            created_at=datetime.utcnow()
        )
        
        db.session.add(junior_ustad)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'জুনিয়র উস্তাদ অ্যাকাউন্ট তৈরি হয়েছে',
            'data': {
                'id': junior_ustad.id,
                'name': f"{junior_ustad.first_name} {junior_ustad.last_name}",
                'phone': junior_ustad.phoneNumber
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@junior_ustad_bp.route('/<int:id>', methods=['PUT'])
@admin_required
def update_junior_ustad(id):
    """Update junior ustad account"""
    try:
        junior_ustad = User.query.filter_by(
            id=id,
            role=UserRole.JUNIOR_USTADH
        ).first()
        
        if not junior_ustad:
            return jsonify({
                'success': False,
                'error': 'জুনিয়র উস্তাদ পাওয়া যায়নি'
            }), 404
        
        data = request.get_json()
        
        # Update fields
        if 'first_name' in data:
            junior_ustad.first_name = data['first_name']
        if 'last_name' in data:
            junior_ustad.last_name = data['last_name']
        if 'phone' in data:
            # Check if new phone is already taken by another user
            existing = User.query.filter(
                User.phoneNumber == data['phone'],
                User.id != id
            ).first()
            if existing:
                return jsonify({
                    'success': False,
                    'error': 'এই ফোন নম্বর ইতিমধ্যে ব্যবহৃত হয়েছে'
                }), 400
            junior_ustad.phoneNumber = data['phone']
        if 'email' in data:
            junior_ustad.email = data['email']
        if 'password' in data and data['password']:
            junior_ustad.password_hash = generate_password_hash(data['password'])
        if 'is_active' in data:
            junior_ustad.is_active = data['is_active']
        
        junior_ustad.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'জুনিয়র উস্তাদ আপডেট হয়েছে',
            'data': {
                'id': junior_ustad.id,
                'name': f"{junior_ustad.first_name} {junior_ustad.last_name}",
                'phone': junior_ustad.phoneNumber
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@junior_ustad_bp.route('/<int:id>', methods=['DELETE'])
@admin_required
def delete_junior_ustad(id):
    """Delete (archive) junior ustad account"""
    try:
        junior_ustad = User.query.filter_by(
            id=id,
            role=UserRole.JUNIOR_USTADH
        ).first()
        
        if not junior_ustad:
            return jsonify({
                'success': False,
                'error': 'জুনিয়র উস্তাদ পাওয়া যায়নি'
            }), 404
        
        # Archive instead of delete
        junior_ustad.is_archived = True
        junior_ustad.archived_at = datetime.utcnow()
        junior_ustad.archived_by = session['user_id']
        junior_ustad.archive_reason = 'Admin deleted junior ustad account'
        junior_ustad.is_active = False
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'জুনিয়র উস্তাদ অ্যাকাউন্ট মুছে ফেলা হয়েছে'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@junior_ustad_bp.route('/<int:id>/toggle-status', methods=['POST'])
@admin_required
def toggle_junior_ustad_status(id):
    """Toggle active/inactive status of junior ustad"""
    try:
        junior_ustad = User.query.filter_by(
            id=id,
            role=UserRole.JUNIOR_USTADH
        ).first()
        
        if not junior_ustad:
            return jsonify({
                'success': False,
                'error': 'জুনিয়র উস্তাদ পাওয়া যায়নি'
            }), 404
        
        junior_ustad.is_active = not junior_ustad.is_active
        junior_ustad.updated_at = datetime.utcnow()
        db.session.commit()
        
        status = 'সক্রিয়' if junior_ustad.is_active else 'নিষ্ক্রিয়'
        
        return jsonify({
            'success': True,
            'message': f'জুনিয়র উস্তাদ অ্যাকাউন্ট {status} করা হয়েছে',
            'data': {'is_active': junior_ustad.is_active}
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
