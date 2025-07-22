from .models import db, Company, Conference
from datetime import datetime

def init_database(app):
    """Initialize database and create sample data"""
    with app.app_context():
        db.create_all()
        
        # Add sample data if database is empty
        if Company.query.count() == 0:
            create_sample_data()

def create_sample_data():
    """Create sample companies and conferences"""
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

def reset_database(app):
    """Drop all tables and recreate them (useful for development)"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_sample_data()