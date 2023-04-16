from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_login import LoginManager

from .models.User import User
from .config import Config
from .send_email import send_email, mail

import os

scheduler = BackgroundScheduler()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('DEV_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_DEV_URI')

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.update(test_config)

    from .models.base import db

    db.init_app(app)

    from .auth import auth
    from .views import views

    app.register_blueprint(views)
    app.register_blueprint(auth)

    with app.app_context():
        if not app.config.get('SCHEDULER_RUNNING', False):
            scheduler.start()
            scheduler.add_job(send_email, 'interval', minutes=1, args=(app,))
            app.config['SCHEDULER_RUNNING'] = True

        db.create_all()
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = 'auth.login'
        mail.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))
    return app
