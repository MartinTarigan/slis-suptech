from flask import Flask
from slis.db import Base, engine
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig

db = SQLAlchemy()


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register blueprints
    from slis.routes.transactions import transactions_bp
    from slis.routes.sanctions import sanctions_bp
    from slis.routes.screening import screening_bp
    from slis.routes.web import web_bp


    app.register_blueprint(transactions_bp, url_prefix="/api/batches")
    app.register_blueprint(sanctions_bp, url_prefix="/api/sanctions")
    app.register_blueprint(screening_bp, url_prefix='/api/screening')
    
    app.register_blueprint(web_bp)

    return app
