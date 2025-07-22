from flask import Blueprint, render_template
from ..models import Company, Conference, Booking, Payment

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    total_companies = Company.query.count()
    total_conferences = Conference.query.count()
    total_bookings = Booking.query.count()
    pending_payments = Payment.query.filter_by(payment_status='Pending').count()

    recent_conferences = Conference.query.order_by(Conference.created_date.desc()).limit(5).all()
    recent_bookings = Booking.query.order_by(Booking.booking_date.desc()).limit(5).all()

    return render_template('dashboard.html',
                           total_companies=total_companies,
                           total_conferences=total_conferences,
                           total_bookings=total_bookings,
                           pending_payments=pending_payments,
                           recent_conferences=recent_conferences,
                           recent_bookings=recent_bookings)
