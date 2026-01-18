from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='tenant') # 'admin' or 'tenant'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='available') # available, occupied, maintenance
    facilities = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    
    # Relationship to Tenant
    tenants = db.relationship('Tenant', backref='room', lazy=True)

class Tenant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=True)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    entry_date = db.Column(db.Date, default=datetime.utcnow().date)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    user = db.relationship('User', backref=db.backref('tenant_profile', uselist=False))
    payments = db.relationship('Payment', backref='tenant', lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenant.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    billing_month = db.Column(db.String(50))
    status = db.Column(db.String(20), default='pending') # pending, verified, rejected
    proof_of_payment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    occupation = db.Column(db.String(50))
    room_type = db.Column(db.String(50), nullable=False)
    checkin_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending') # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
