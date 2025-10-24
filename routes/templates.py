"""
Template Routes
HTML template rendering for frontend pages
"""
from flask import Blueprint, render_template, redirect, url_for, session, request

templates_bp = Blueprint('templates', __name__)

@templates_bp.route('/')
def index():
    """Landing page - redirects based on login status and role"""
    try:
        # Check if user is logged in
        if 'user' in session and session['user']:
            user_role = session['user'].get('role')
            
            if user_role == 'student':
                return render_template('dashboard_student_new.html', user=session['user'])
            elif user_role == 'teacher':
                return render_template('dashboard_teacher.html', user=session['user'])
            elif user_role == 'junior_ustadh':
                return render_template('dashboard_junior_ustad.html', user=session['user'])
            elif user_role == 'super_user':
                # Super users get their own dashboard
                return render_template('dashboard_super_admin_simple.html', user=session['user'])
    except (KeyError, AttributeError, TypeError) as e:
        # Clear invalid session data
        session.clear()
    
    # Not logged in, show landing page
    return render_template('index.html')

@templates_bp.route('/debug-fees')
def debug_fees():
    """Debug page for fees feature"""
    try:
        with open('debug_fees.html', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "<h1>Debug fees page not found</h1><p>The debug_fees.html file was not found.</p>", 404

@templates_bp.route('/test-fee-save')
def test_fee_save():
    """Test page for fee save endpoint"""
    return render_template('test_fee_save.html')

@templates_bp.route('/login')
def login_page():
    """Login page"""
    
    return render_template('login.html')

@templates_bp.route('/dashboard')
def dashboard():
    """Main dashboard - same as index, redirects based on role"""
    return redirect(url_for('templates.index'))

@templates_bp.route('/student')
def student_dashboard():
    """Student dashboard direct route"""
    if 'user' not in session:
        return redirect(url_for('templates.login_page'))
    
    user_role = session['user'].get('role')
    if user_role != 'student':
        return redirect(url_for('templates.index'))
    
    return render_template('dashboard_student_new.html', user=session['user'])

@templates_bp.route('/teacher')  
def teacher_dashboard():
    """Teacher dashboard direct route"""
    if 'user' not in session:
        return redirect(url_for('templates.login_page'))
    
    user_role = session['user'].get('role')
    if user_role != 'teacher':
        return redirect(url_for('templates.index'))
    
    return render_template('dashboard_teacher.html', user=session['user'])

@templates_bp.route('/super')
def super_dashboard():
    """Super user dashboard direct route"""
    if 'user' not in session:
        return redirect(url_for('templates.login_page'))
    
    user_role = session['user'].get('role')
    if user_role != 'super_user':
        return redirect(url_for('templates.index'))
    
    return render_template('dashboard_super_admin_simple.html', user=session['user'])

@templates_bp.route('/junior-ustadh')
def junior_ustadh_dashboard():
    """Junior ustadh (assistant teacher) dashboard direct route"""
    if 'user' not in session:
        return redirect(url_for('templates.login_page'))
    
    user_role = session['user'].get('role')
    if user_role != 'junior_ustadh':
        return redirect(url_for('templates.index'))
    
    return render_template('dashboard_junior_ustad.html', user=session['user'])

@templates_bp.route('/junior-ustad-management')
def junior_ustad_management():
    """Junior ustadh management page (admin and senior teachers)"""
    if 'user' not in session:
        return redirect(url_for('templates.login_page'))
    
    user_role = session['user'].get('role')
    if user_role not in ['super_user', 'teacher']:
        return redirect(url_for('templates.index'))
    
    return render_template('junior_ustad_management.html', user=session['user'])

@templates_bp.route('/test-junior-ustad')
def test_junior_ustad():
    """Test page for junior ustad API"""
    return render_template('test_junior_ustad.html')

@templates_bp.route('/junior-ustad-simple')
def junior_ustad_simple():
    """Simple version of junior ustad management (no Alpine.js)"""
    if 'user' not in session:
        return redirect(url_for('templates.login_page'))
    
    user_role = session['user'].get('role')
    if user_role not in ['super_user', 'teacher']:
        return redirect(url_for('templates.index'))
    
    return render_template('junior_ustad_simple.html', user=session['user'])