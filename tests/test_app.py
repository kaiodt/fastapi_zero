from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fastapi_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_must_return_hello_world(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello, world!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'User',
            'email': 'user@example.com',
            'password': 'secret123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'User',
        'email': 'user@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'User',
                'email': 'user@example.com',
                'id': 1,
            }
        ]
    }


def test_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'User',
        'email': 'user@example.com',
        'id': 1,
    }


def test_read_unexisting_user_should_return_not_found(client):
    response = client.get('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'Other User',
            'email': 'other_user@example.com',
            'password': 'newsecret123',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Other User',
        'email': 'other_user@example.com',
        'id': 1,
    }


def test_update_unexisting_user_should_return_not_found(client):
    response = client.put(
        '/users/100',
        json={
            'username': 'Unknown',
            'email': 'unknown@example.com',
            'password': 'nobody123',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_unexisting_user_should_return_not_found(client):
    response = client.delete('/users/100')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
