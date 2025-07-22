def register_routes(app):
    from .dashboard import bp as dashboard_bp
    from .companies import bp as companies_bp
    from .conferences import bp as conferences_bp
    from .bookings import bp as bookings_bp
    from .payments import bp as payments_bp
    from .api import bp as api_bp
    
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(conferences_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(api_bp)