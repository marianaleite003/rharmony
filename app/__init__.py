from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')

    db.init_app(app)
    Bootstrap(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.login_message = "Por favor, faça o login para acessar esta página."
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    from .models import Gestor

    @login_manager.user_loader
    def load_user(user_id):
        return Gestor.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    return app