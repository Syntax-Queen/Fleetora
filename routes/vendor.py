from app import app
from flask import jsonify, request

from models import vendor, db
from toolz import validate_email

@app.route('/vendors', methods=['POST'])
def signup():
    data = request.json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if email is None or password is None or name is None:
        return jsonify({'message': 'Missing required fields'}), 400
    
    if name is None or len(name) < 3:
        return jsonify({'message': 'Name must be at least 3 characters long'}), 400     
    
    
    if not validate_email(email ) or email is None:
        return jsonify({'message': 'Invalid email format'}), 400
    

    if vendor.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_vendor = vendor(name=name, email=email)
    db.session.add(new_vendor)
    new_vendor.set_password(password)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Vendor registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500    
