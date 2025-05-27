from http import HTTPStatus

from jwt import decode

from fastapi_zero.security import SECRET_KEY, create_access_token


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded


def test_get_current_user_invalid_jwt_token(client):
    response = client.delete(
        '/users/1',
        headers={'Authorization': 'Bearer invalid-token'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_missing_email(client):
    bad_token = create_access_token(
        data={'no-email': 'test'},
    )

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {bad_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_unexisting_user(client):
    bad_token = create_access_token(
        data={'sub': 'unknown@test.com'},
    )

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {bad_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
