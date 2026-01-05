from flask_cors import cross_origin
from app import app
from flask import jsonify, request

from models import PasswordResetToken, StoredjwtToken, Vendor, db
from toolz import random_generator, validate_email

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
    

    if Vendor.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already registered'}), 400

    new_vendor = Vendor(name=name, email=email)
    db.session.add(new_vendor)
    new_vendor.set_password(password)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Vendor registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Registration failed', 'error': str(e)}), 500    



@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    user = Vendor.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User with this email does not exist'}), 404

    if not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 400

    # Remove old token if it exists
    saved_token = StoredjwtToken.query.filter_by(user_id=user.id).first()
    if saved_token:
        db.session.delete(saved_token)
        db.session.commit()

    # Generate new token
    token = user.generate_auth_token()
    new_jwt_token = StoredjwtToken(user_id=user.id, jwt_token=token)
    db.session.add(new_jwt_token)
    db.session.commit()

    return jsonify({'success': True, 'token': token}), 200


# forget password
@app.route('/forget-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    
    # check if email exists
    if email is None:
        return jsonify({'error': 'Please enter email'}), 400
    
    user = Vendor.query.filter_by(email=email).first()
    if user is None:
        return jsonify({'error': 'User with this email does not exist'}), 400
    
    # create a password reset token
    token = random_generator(8)
    reset = PasswordResetToken(token=token, user_id=user.id, used=False)
    db.session.add(reset)
    db.session.commit()
    
    # send password reset token to email
    return jsonify({'success': True, 'message': 'Password reset email sent'}), 200

# reset password
@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.json.get('token')
    new_password = request.json.get('new_password')
    confirm_password = request.json.get('confirm_password')
    
    if new_password is None or confirm_password != new_password:
        return jsonify({'error': 'Password does not match'}), 400
    
    if token is None:
        return jsonify({'error': 'Please enter token'}), 400
    
    reset = PasswordResetToken.query.filter_by(token=token).first()
    if reset is None:
        return jsonify({'error': 'Invalid token'}), 400
    
    if reset.used:
        return jsonify({'error': 'Token has been used already'}), 400
    
    user = Vendor.query.filter_by(id=reset.user_id).first()
    if user is None:
        return jsonify({'error':' User not found'}), 400
    
    user.set_password(new_password)
    reset.used = True
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Password reset successfully'}), 200


# delete users
@app.route('/<int:did>', methods=['DELETE'])
def delete_user(did):
    user = Vendor.query.filter(Vendor.id == did).first()
    if user is None:
        return jsonify({'error': 'User does not exit'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'done': True, 'Message': f'{user.name} Account deleted successfully'})


# edit username and password 

@app.route('/vendors/<int:vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    data = request.json

    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        return jsonify({'message': 'Vendor not found'}), 404

    name = data.get('name')
    password = data.get('password')

    if name:
        if len(name) < 3:
            return jsonify({'message': 'Name must be at least 3 characters long'}), 400
        vendor.name = name

    if password:
        vendor.set_password(password)

    try:
        db.session.commit()
        return jsonify({'message': 'Vendor updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Update failed', 'error': str(e)}), 500
