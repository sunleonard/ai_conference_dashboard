from flask import Blueprint, jsonify
from ..models import Company, Conference

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/companies')
def companies():
    companies = Company.query.all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'industry': c.industry,
        'website': c.website
    } for c in companies])

@bp.route('/conferences')
def conferences():
    conferences = Conference.query.all()
    return jsonify([{
        'id': c.id,
        'title': c.title,
        'start_date': c.start_date.isoformat(),
        'end_date': c.end_date.isoformat(),
        'location': c.location,
        'price': c.price
    } for c in conferences])