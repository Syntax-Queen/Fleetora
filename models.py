import datetime
import os
from time import timezone
import jwt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime,  default=lambda: datetime.now(timezone.utc) )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_auth_token(self):
        expiration_time = datetime.now() + datetime.timedelta(days=10)
        payload ={
            'id': self.id,
            'exp': expiration_time,
            # 'role': self.role
        }
        
        token = jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')
        return token
    
    @staticmethod
    def verify_auth_token(token):
        if not token:
            return None
        try:
            active_token = StoredjwtToken.query.filter_by(jwt_token=token).first()
            if active_token:
                payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=['HS256'])
                user = Vendor.query.get(payload['id'])
                return user
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.DecodeError:
            print("Token is invalid")
            return None
        
        

class StoredjwtToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jwt_token = db.Column(db.String(255), unique=True, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
       