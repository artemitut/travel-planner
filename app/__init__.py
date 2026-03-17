from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # конфіг
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ініціалізація БД
    db.init_app(app)

    # реєстрація роутів
    from .routes.projects import projects_bp
    from .routes.places import places_bp

    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(places_bp, url_prefix='/places')

    return app
