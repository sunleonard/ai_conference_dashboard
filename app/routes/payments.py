from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Payment, Booking, Conference
from datetime import datetime

bp = Blueprint('payments', __name__, url_prefix='/payments')

@bp.route('/')
def index():
    # Fix: Add proper joins to get booking and conference data
    payments = Payment.query.join(Booking).join(Conference).all()
    
    # Calculate payment summaries in Python instead of Jinja2
    completed_total = sum(p.amount for p in payments if p.payment_status == 'Completed')
    pending_total = sum(p.amount for p in payments if p.payment_status == 'Pending')
    failed_total = sum(p.amount for p in payments if p.payment_status == 'Failed')
    
    return render_template('payments.html', 
                         payments=payments,
                         completed_total=completed_total,
                         pending_total=pending_total,
                         failed_total=failed_total)

@bp.route('/<int:payment_id>/update_status', methods=['POST'])
def update_status(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    new_status = request.form['status']
    payment.payment_status = new_status

    if new_status == 'Completed':
        payment.payment_date = datetime.utcnow()
        payment.transaction_id = f"TXN{payment_id}{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    db.session.commit()
    flash(f'Payment status updated to {new_status}!', 'success')
    return redirect(url_for('payments.index'))