from web.send_email import send_email
import pytest


def test_send_email(client, app, login, capsys):
    with app.test_request_context():
        send_email(app)
        captured = capsys.readouterr()
        assert 'mail sent!!' in captured.out
