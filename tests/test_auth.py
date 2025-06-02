from http import HTTPStatus


def test_get_token(client, user):
    response = client.post(
        'auth/token/',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_for_unexisting_user_should_return_unauthorized(client):
    response = client.post(
        'auth/token/',
        data={
            'username': 'unknown@email.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_get_token_wrong_password_should_return_unauthorized(client, user):
    response = client.post(
        'auth/token/',
        data={
            'username': user.email,
            'password': 'wrong_password',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect email or password'}
