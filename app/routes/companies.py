from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..models import db, Company, CompanyDetails, BusinessIntelligence
from datetime import datetime

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
        db.session.flush()  # Get company ID before commit
        
        # Create company details if any data is provided
        details = CompanyDetails(
            company_id=company.id,
            founded_year=int(request.form['founded_year']) if request.form['founded_year'] else None,
            num_employees=int(request.form['num_employees']) if request.form['num_employees'] else None,
            annual_revenue=float(request.form['annual_revenue']) if request.form['annual_revenue'] else None,
            headquarters=request.form['headquarters'] if request.form['headquarters'] else None,
            funding_stage=request.form['funding_stage'] if request.form['funding_stage'] else None
        )
        db.session.add(details)
        
        db.session.commit()
        flash('Company added successfully!', 'success')
        # Redirect to the newly created company's detail page
        return redirect(url_for('companies.detail', id=company.id))

    return render_template('add_company.html')

@bp.route('/<int:id>')
def detail(id):
    company = Company.query.get_or_404(id)
    # Get or create company details
    details = CompanyDetails.query.filter_by(company_id=id).first()
    if not details:
        details = CompanyDetails(company_id=id)
        db.session.add(details)
        db.session.commit()
    
    # Get business intelligence data
    intelligence = BusinessIntelligence.query.filter_by(company_id=id).all()
    
    return render_template('company_detail.html', 
                         company=company, 
                         details=details,
                         intelligence=intelligence)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    company = Company.query.get_or_404(id)
    details = CompanyDetails.query.filter_by(company_id=id).first()
    
    if not details:
        details = CompanyDetails(company_id=id)
        db.session.add(details)
        db.session.commit()
    
    if request.method == 'POST':
        # Update company basic info
        company.name = request.form['name']
        company.industry = request.form['industry']
        company.website = request.form['website']
        company.contact_email = request.form['contact_email']
        company.phone = request.form['phone']
        company.description = request.form['description']
        
        # Update company details
        details.founded_year = int(request.form['founded_year']) if request.form['founded_year'] else None
        details.num_employees = int(request.form['num_employees']) if request.form['num_employees'] else None
        details.annual_revenue = float(request.form['annual_revenue']) if request.form['annual_revenue'] else None
        details.headquarters = request.form['headquarters'] if request.form['headquarters'] else None
        details.funding_stage = request.form['funding_stage'] if request.form['funding_stage'] else None
        
        db.session.commit()
        flash('Company updated successfully!', 'success')
        return redirect(url_for('companies.detail', id=id))
    
    return render_template('edit_company.html', company=company, details=details)

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    company = Company.query.get_or_404(id)
    
    # Check if company has associated conferences or bookings
    if company.conferences or company.bookings:
        flash('Cannot delete company with associated conferences or bookings!', 'danger')
        return redirect(url_for('companies.detail', id=id))
    
    # Delete associated details and intelligence
    CompanyDetails.query.filter_by(company_id=id).delete()
    BusinessIntelligence.query.filter_by(company_id=id).delete()
    
    db.session.delete(company)
    db.session.commit()
    flash(f'Company "{company.name}" deleted successfully!', 'success')
    return redirect(url_for('companies.index'))

@bp.route('/<int:id>/add_intelligence', methods=['POST'])
def add_intelligence(id):
    company = Company.query.get_or_404(id)
    
    intelligence = BusinessIntelligence(
        company_id=id,
        insight_type=request.form['insight_type'],
        insight_text=request.form['insight_text'],
        source=request.form['source']
    )
    db.session.add(intelligence)
    db.session.commit()
    
    flash('Business intelligence added successfully!', 'success')
    return redirect(url_for('companies.detail', id=id))

@bp.route('/intelligence/<int:id>/delete', methods=['POST'])
def delete_intelligence(id):
    intelligence = BusinessIntelligence.query.get_or_404(id)
    company_id = intelligence.company_id
    
    db.session.delete(intelligence)
    db.session.commit()
    
    flash('Business intelligence deleted successfully!', 'success')
    return redirect(url_for('companies.detail', id=company_id))