import pytest
import json


def test_home(client, app, login):
    with app.test_request_context():
        response = client.post(
            '/', data={'items': 'Buy clothes', 'datetime': '2023-05-20 13:00'})
        assert ('Item added') in response.text

        response = client.get('/')
        assert('Buy clothes') in response.text
        assert('2023-05-20 13:00') in response.text


@pytest.mark.parametrize(
    "items, datetime, message",
    [('', '2023-04-30 12:00', 'Please enter a description!'),
     ('Watch movie', '', 'Please select a date!')
     ]
)
def test_home_validate_input(client, app, login, items, datetime, message):
    with app.test_request_context():
        response = client.post(
            '/', data={'items': items, 'datetime': datetime})
        assert message in response.text


def test_update_item(client, app, login):
    with app.test_request_context():
        response = client.patch(
            '/update-item', data=json.dumps({'itemId': 1, 'description': 'Buy beers', 'date': '2023-04-20 13:00'}))
        assert all(item in response.text for item in [
                   'Item updated', 'Buy beers', '2023-04-20 13:00', 'false'])


def test_delete_item(client, app, login):
    with app.test_request_context():
        response = client.delete(
            '/delete-item', data=json.dumps({'itemId': 1}))
        assert all(item in response.text for item in ['Item deleted', '1'])
