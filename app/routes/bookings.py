from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Booking, Company, Conference, Payment
from datetime import datetime

bp = Blueprint('bookings', __name__, url_prefix='/bookings')

@bp.route('/')
def index():
    bookings = Booking.query.join(Conference).join(Company).all()
    return render_template('bookings.html', bookings=bookings)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        booking = Booking(
            attendee_name=request.form['attendee_name'],
            attendee_email=request.form['attendee_email'],
            attendee_phone=request.form['attendee_phone'],
            conference_id=int(request.form['conference_id']),
            company_id=int(request.form['company_id']),
        )
        db.session.add(booking)
        db.session.commit()

        conference = Conference.query.get(booking.conference_id)
        payment = Payment(
            amount=conference.price,
            booking_id=booking.id
        )
        db.session.add(payment)
        db.session.commit()

        flash('Booking added successfully!', 'success')
        return redirect(url_for('bookings.index'))

    conferences = Conference.query.filter_by(status='Active').all()
    companies = Company.query.all()
    return render_template('add_booking.html', conferences=conferences, companies=companies)
