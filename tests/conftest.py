from werkzeug.security import generate_password_hash
from web.models.base import db
from web.models.User import User
from web.models.Item import Item
from datetime import datetime, timedelta
from web import create_app
from web import scheduler
from dotenv import load_dotenv

import pytest
import os

load_dotenv()


@pytest.fixture()
def app():
    app = create_app(
        {"TESTING": True,
         'SQLALCHEMY_DATABASE_URI': os.environ.get('SQLALCHEMY_DATABASE_TEST_URI'),
         'SECRET_KEY': os.environ.get('TEST_SECRET_KEY'),
         'MAIL_DEFAULT_SENDER': os.environ.get('MAIL_DEFAULT_SENDER')})

    with app.app_context():
        db.create_all()
        user = User(email='test@example.com',
                    name='test', password=generate_password_hash(
                        'testtest', method='sha256'))
        item = Item(description='Test Item', date=datetime.now() -
                    timedelta(minutes=30), is_expired=False)

        user.items.append(item)
        db.session.add(user)
        db.session.add(item)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()
        scheduler.shutdown()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def login(client):
    return client.post(
        '/login', data={'email': 'test@example.com', 'password': 'testtest'}, follow_redirects=True)
