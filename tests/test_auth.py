from flask import url_for
import pytest



def test_register(client, app):
    with app.test_request_context():
        assert client.get("/register").status_code == 200

        response = client.post(
            "/register", data={"email": "test@gmail.com", "name": "test", "password1": "testtest", "password2": "testtest"}, follow_redirects=True)
        assert len(response.history) == 1
        assert ('Account created!') in response.text
        assert response.request.path == url_for('views.home')


@pytest.mark.parametrize(
    "email, name, password1, password2, message",
    [("test@example.com", "test", "testtest", "testtest", "Email already exists"),
     ("ann", "test", "testtest", "testtest",
      "Email must be at least 4 characters"),
     ("test@gmail.com", "a", "testtest", "testtest",
      "Name must be at least 2 characters"),
     ("test@gmail.com", "test", "testtest",
      "testtetsege", "Password don&#39;t match"),
     ("test@gmail.com", "test", "testte", "testte",
      "Password must be at least 7 characters")
     ]
)
def test_register_validate_input(client, app, email, name, password1, password2, message):
    with app.test_request_context():
        response = client.post(
            "/register", data={"email": email, "name": name, "password1": password1, "password2": password2}, follow_redirects=True)
        assert message in response.text


def test_login(client, app):
    with app.test_request_context():
        assert client.get("/login").status_code == 200

        response = client.post(
            '/login', data={'email': 'test@example.com', 'password': 'testtest'}, follow_redirects=True)
        assert len(response.history) == 1
        assert ('Logged in successfully!') in response.text
        assert response.request.path == url_for('views.home')


@pytest.mark.parametrize(
    "email, password, message",
    [("a", "password", "Email does not exist"),
     ("test@example.com", "a", "Incorrect password, try again!")]
)
def test_login_validate_input(client, app, email, password, message):
    with app.test_request_context():
        response = client.post(
            '/login', data={'email': email, 'password': password}, follow_redirects=True)
        assert message in response.text


def test_logout(client, app, login):
    with app.test_request_context():
        response = client.get('/logout', follow_redirects=True)
        assert len(response.history) == 1
        assert ('Logged out successfully!') in response.text
        assert response.request.path == url_for('auth.login')
