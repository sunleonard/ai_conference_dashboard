from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import db, Company

bp = Blueprint('companies', __name__, url_prefix='/companies')

@bp.route('/')
def index():
    companies = Company.query.all()
    return render_template('companies.html', companies=companies)

@bp.route('/add', methods=['GET', 'POST'])
def add():
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
        return redirect(url_for('companies.index'))

    return render_template('add_company.html')
