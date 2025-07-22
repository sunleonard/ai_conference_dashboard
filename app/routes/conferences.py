from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Conference, Company
from datetime import datetime

bp = Blueprint('conferences', __name__, url_prefix='/conferences')

@bp.route('/')
def index():
    conferences = Conference.query.join(Company).all()
    return render_template('conferences.html', conferences=conferences)

@bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
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
            return redirect(url_for('conferences.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    companies = Company.query.all()
    return render_template('add_conference.html', companies=companies)
