from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()

db = SQLAlchemy()
DB_NAME = os.getenv('DB_NAME')
LOCALHOST_PASS = os.getenv('LOCALHOST_PASS')
LOCALHOST_USER = os.getenv('LOCALHOST_USER')
SECRET_KEY = os.getenv('SECRET_KEY')


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{LOCALHOST_USER}:{LOCALHOST_PASS}@localhost/{DB_NAME}'
    db.init_app(app)
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    @loginManager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')


mail = Mail(create_app())
