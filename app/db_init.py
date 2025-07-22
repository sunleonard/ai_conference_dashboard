from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False, default='Artificial Intelligence')
    website = db.Column(db.String(200))
    contact_email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    conferences = db.relationship('Conference', backref='organizer', lazy=True)
    bookings = db.relationship('Booking', backref='company', lazy=True)
    users = db.relationship('User', backref='company', lazy=True)
    details = db.relationship('CompanyDetails', backref='company', uselist=False, lazy=True)
    intelligence = db.relationship('BusinessIntelligence', backref='company', lazy=True)

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    max_attendees = db.Column(db.Integer, default=100)
    status = db.Column(db.String(20), default='Active')
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='conference', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendee_name = db.Column(db.String(100), nullable=False)
    attendee_email = db.Column(db.String(100), nullable=False)
    attendee_phone = db.Column(db.String(20))
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    payment = db.relationship('Payment', backref='booking', uselist=False, lazy=True)
    invoice = db.relationship('Invoice', backref='booking', uselist=False, lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='Credit Card')
    payment_status = db.Column(db.String(20), default='Pending')
    payment_date = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(100))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='Unpaid')
    subtotal = db.Column(db.Float)
    tax = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='attendee')
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class CompanyDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False, unique=True)
    founded_year = db.Column(db.Integer)
    num_employees = db.Column(db.Integer)
    annual_revenue = db.Column(db.Float)
    headquarters = db.Column(db.String(150))
    funding_stage = db.Column(db.String(50))

class BusinessIntelligence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    insight_type = db.Column(db.String(100))
    insight_text = db.Column(db.Text)
    source = db.Column(db.String(200))
    collected_date = db.Column(db.DateTime, default=datetime.utcnow)
