from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conference_dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Models
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False, default='Artificial Intelligence')
    website = db.Column(db.String(200))
    contact_email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    conferences = db.relationship('Conference', backref='organizer', lazy=True)
    bookings = db.relationship('Booking', backref='company', lazy=True)

class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    max_attendees = db.Column(db.Integer, default=100)
    status = db.Column(db.String(20), default='Active')  # Active, Completed, Cancelled
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='conference', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    attendee_name = db.Column(db.String(100), nullable=False)
    attendee_email = db.Column(db.String(100), nullable=False)
    attendee_phone = db.Column(db.String(20))
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='Pending')  # Pending, Confirmed, Cancelled
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    
    # Relationships
    payment = db.relationship('Payment', backref='booking', uselist=False, lazy=True)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), default='Credit Card')
    payment_status = db.Column(db.String(20), default='Pending')  # Pending, Completed, Failed, Refunded
    payment_date = db.Column(db.DateTime)
    transaction_id = db.Column(db.String(100))
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def dashboard():
    # Dashboard statistics
    total_companies = Company.query.count()
    total_conferences = Conference.query.count()
    total_bookings = Booking.query.count()
    pending_payments = Payment.query.filter_by(payment_status='Pending').count()
    
    # Recent activities
    recent_conferences = Conference.query.order_by(Conference.created_date.desc()).limit(5).all()
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         total_companies=total_companies,
                         total_conferences=total_conferences,
                         total_bookings=total_bookings,
                         pending_payments=pending_payments,
                         recent_conferences=recent_conferences,
                         recent_bookings=recent_bookings)

# Company Management Routes
@app.route('/companies')
def companies():
    companies = Company.query.all()
    return render_template('companies.html', companies=companies)

@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company = Company(
            name=request.form['name'],
            industry=request.form['industry'],
            website=request.form['website'],
            contact_email=request.form['contact_email'],
            phone=request.form['phone'],
            description=request.form['description']
        )
        db.session.add(company)
        db.session.commit()
        flash('Company added successfully!', 'success')
        return redirect(url_for('companies'))
    return render_template('add_company.html')

# Conference Management Routes
@app.route('/conferences')
def conferences():
    conferences = Conference.query.join(Company).all()
    return render_template('conferences.html', conferences=conferences)

@app.route('/conferences/add', methods=['GET', 'POST'])
def add_conference():
    if request.method == 'POST':
        conference = Conference(
            title=request.form['title'],
            description=request.form['description'],
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M'),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M'),
            location=request.form['location'],
            price=float(request.form['price']),
            max_attendees=int(request.form['max_attendees']),
            company_id=int(request.form['company_id'])
        )
        db.session.add(conference)
        db.session.commit()
        flash('Conference added successfully!', 'success')
        return redirect(url_for('conferences'))
    
    companies = Company.query.all()
    return render_template('add_conference.html', companies=companies)

# Booking Management Routes
@app.route('/bookings')
def bookings():
    bookings = Booking.query.join(Conference).join(Company).all()
    return render_template('bookings.html', bookings=bookings)

@app.route('/bookings/add', methods=['GET', 'POST'])
def add_booking():
    if request.method == 'POST':
        booking = Booking(
            attendee_name=request.form['attendee_name'],
            attendee_email=request.form['attendee_email'],
            attendee_phone=request.form['attendee_phone'],
            conference_id=int(request.form['conference_id']),
            company_id=int(request.form['company_id'])
        )
        db.session.add(booking)
        db.session.commit()
        
        # Create associated payment record
        conference = Conference.query.get(int(request.form['conference_id']))
        payment = Payment(
            amount=conference.price,
            booking_id=booking.id
        )
        db.session.add(payment)
        db.session.commit()
        
        flash('Booking added successfully!', 'success')
        return redirect(url_for('bookings'))
    
    conferences = Conference.query.filter_by(status='Active').all()
    companies = Company.query.all()
    return render_template('add_booking.html', conferences=conferences, companies=companies)

# Payment Management Routes
@app.route('/payments')
def payments():
    payments = Payment.query.join(Booking).join(Conference).all()
    return render_template('payments.html', payments=payments)

@app.route('/payments/<int:payment_id>/update_status', methods=['POST'])
def update_payment_status(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    new_status = request.form['status']
    payment.payment_status = new_status
    if new_status == 'Completed':
        payment.payment_date = datetime.utcnow()
        payment.transaction_id = f"TXN{payment_id}{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    db.session.commit()
    flash(f'Payment status updated to {new_status}!', 'success')
    return redirect(url_for('payments'))

# API Routes for AJAX calls
@app.route('/api/companies')
def api_companies():
    companies = Company.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'industry': c.industry,
        'website': c.website
    } for c in companies])

@app.route('/api/conferences')
def api_conferences():
    conferences = Conference.query.all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'start_date': c.start_date.isoformat(),
        'end_date': c.end_date.isoformat(),
        'location': c.location,
        'price': c.price
    } for c in conferences])

# Initialize database function
def init_database():
    db.create_all()
    
    # Add sample data if database is empty
    if Company.query.count() == 0:
        # Sample companies
        companies = [
            Company(name="OpenAI", industry="Artificial Intelligence", website="https://openai.com", 
                   contact_email="contact@openai.com", description="Leading AI research company"),
            Company(name="DeepMind", industry="Artificial Intelligence", website="https://deepmind.com", 
                   contact_email="contact@deepmind.com", description="AI research lab owned by Google"),
            Company(name="Anthropic", industry="Artificial Intelligence", website="https://anthropic.com", 
                   contact_email="contact@anthropic.com", description="AI safety company")
        ]
        
        for company in companies:
            db.session.add(company)
        db.session.commit()
        
        # Sample conferences
        conferences = [
            Conference(title="AI Safety Summit 2025", description="Annual AI safety conference",
                      start_date=datetime(2025, 10, 15, 9, 0),
                      end_date=datetime(2025, 10, 17, 18, 0),
                      location="San Francisco, CA", price=599.0, max_attendees=200,
                      company_id=3),  # Anthropic
            Conference(title="GPT Developer Conference", description="Latest in GPT technology",
                      start_date=datetime(2025, 11, 5, 10, 0),
                      end_date=datetime(2025, 11, 7, 17, 0),
                      location="Seattle, WA", price=899.0, max_attendees=500,
                      company_id=1),  # OpenAI
        ]
        
        for conference in conferences:
            db.session.add(conference)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_database()
    app.run(debug=True)