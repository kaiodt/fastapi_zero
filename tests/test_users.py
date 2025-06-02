from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


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


def test_create_user_should_return_conflit_for_existing_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'other_email@example.com',
            'password': 'secret123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Username already exists',
    }


def test_create_user_should_return_conflit_for_existing_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'User',
            'email': user.email,
            'password': 'secret123',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {
        'detail': 'Email already exists',
    }


def test_read_users(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        '/users/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_user(client, user, token):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_unexisting_user_should_return_not_found(client, token):
    response = client.get(
        '/users/100',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
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
        'id': user.id,
    }


def test_update_other_user_should_return_forbidden(client, token):
    response = client.put(
        '/users/100',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Unknown',
            'email': 'unknown@example.com',
            'password': 'nobody123',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_integrity_error(client, user, token):
    client.post(
        '/users/',
        json={
            'username': 'User',
            'email': 'user@email.com',
            'password': 'secret123',
        },
    )

    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'User',
            'email': 'new_user@example.com',
            'password': 'newsecret123',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_other_user_should_return_forbidden(client, token):
    response = client.delete(
        '/users/100',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}
