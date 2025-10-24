"""
Junior Ustadh Management Routes
Allows senior ustadh/teacher to manage junior ustadh accounts
"""
from flask import Blueprint, request, jsonify, session
from models import db, User, UserRole
from functools import wraps
from werkzeug.security import generate_password_hash

junior_ustadh_bp = Blueprint('junior_ustadh', __name__)

def teacher_required(f):
    """Decorator to ensure only teachers can access these routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'অনুগ্রহ করে লগইন করুন'}), 401
        
        user = User.query.get(session['user_id'])
        if not user or user.role not in [UserRole.TEACHER, UserRole.SUPER_USER]:
            return jsonify({'success': False, 'error': 'অ্যাক্সেস অস্বীকৃত'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

@junior_ustadh_bp.route('/junior-ustadhs', methods=['GET'])
@teacher_required
def get_junior_ustadhs():
    """Get all junior ustadh accounts"""
    try:
        junior_ustadhs = User.query.filter_by(role=UserRole.JUNIOR_USTADH).all()
        
        data = []
        for ju in junior_ustadhs:
            data.append({
                'id': ju.id,
                'name': ju.name,
                'phone': ju.phone,
                'created_at': ju.created_at.isoformat() if ju.created_at else None,
                'email': ju.email
            })
        
        return jsonify({
            'success': True,
            'data': {
                'junior_ustadhs': data,
                'total': len(data)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@junior_ustadh_bp.route('/junior-ustadhs', methods=['POST'])
@teacher_required
def create_junior_ustadh():
    """Create a new junior ustadh account"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'phone', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field} আবশ্যক'}), 400
        
        # Check if phone already exists
        existing_user = User.query.filter_by(phone=data['phone']).first()
        if existing_user:
            return jsonify({'success': False, 'error': 'এই ফোন নম্বর ইতিমধ্যে ব্যবহৃত হয়েছে'}), 400
        
        # Create new junior ustadh
        junior_ustadh = User(
            name=data['name'],
            phone=data['phone'],
            password_hash=generate_password_hash(data['password']),
            role=UserRole.JUNIOR_USTADH,
            email=data.get('email', '')
        )
        
        db.session.add(junior_ustadh)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'জুনিয়র উস্তাদ সফলভাবে যোগ করা হয়েছে',
            'data': {
                'id': junior_ustadh.id,
                'name': junior_ustadh.name,
                'phone': junior_ustadh.phone
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@junior_ustadh_bp.route('/junior-ustadhs/<int:id>', methods=['PUT'])
@teacher_required
def update_junior_ustadh(id):
    """Update junior ustadh account"""
    try:
        junior_ustadh = User.query.get(id)
        if not junior_ustadh or junior_ustadh.role != UserRole.JUNIOR_USTADH:
            return jsonify({'success': False, 'error': 'জুনিয়র উস্তাদ পাওয়া যায়নি'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            junior_ustadh.name = data['name']
        
        if 'phone' in data and data['phone'] != junior_ustadh.phone:
            # Check if new phone already exists
            existing = User.query.filter_by(phone=data['phone']).first()
            if existing:
                return jsonify({'success': False, 'error': 'এই ফোন নম্বর ইতিমধ্যে ব্যবহৃত হয়েছে'}), 400
            junior_ustadh.phone = data['phone']
        
        if 'email' in data:
            junior_ustadh.email = data['email']
        
        # Update password if provided
        if 'password' in data and data['password']:
            junior_ustadh.password_hash = generate_password_hash(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'জুনিয়র উস্তাদ তথ্য আপডেট করা হয়েছে',
            'data': {
                'id': junior_ustadh.id,
                'name': junior_ustadh.name,
                'phone': junior_ustadh.phone,
                'email': junior_ustadh.email
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@junior_ustadh_bp.route('/junior-ustadhs/<int:id>', methods=['DELETE'])
@teacher_required
def delete_junior_ustadh(id):
    """Delete junior ustadh account"""
    try:
        junior_ustadh = User.query.get(id)
        if not junior_ustadh or junior_ustadh.role != UserRole.JUNIOR_USTADH:
            return jsonify({'success': False, 'error': 'জুনিয়র উস্তাদ পাওয়া যায়নি'}), 404
        
        name = junior_ustadh.name
        db.session.delete(junior_ustadh)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{name} এর অ্যাকাউন্ট মুছে ফেলা হয়েছে'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
