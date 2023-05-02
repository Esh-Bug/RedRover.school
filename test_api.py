import requests
import pytest

BASE_URL = 'https://restful-booker.herokuapp.com/booking'
AUTH_URL = 'https://restful-booker.herokuapp.com/auth'
STATUS_OK = 200


@pytest.fixture(scope='module')
def auth_token():
    payload = {
        "username": "admin",
        "password": "password123"
    }
    response = requests.post(url=AUTH_URL, json=payload)
    # code-style - если указан один параметр с названием, остальные тоже надо
    # передавать с названием(было (AUTH_URL, json=payload))
    if response.status_code != STATUS_OK:  # в фикстуре лучше использовать не ассерт, а эксепшн
        raise Exception(f'Статус код не равен {STATUS_OK}')
    token = response.json()['token']  # сохраняем в переменную значение ключа token
    yield token


@pytest.fixture(scope='module')
def fixture_payload_with_id():
    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"},
        "additionalneeds": "Breakfast"
    }
    response = requests.post(url=BASE_URL, json=payload)

    assert response.status_code == STATUS_OK
    payload['bookingid'] = response.json()['bookingid']

    yield payload


def test_get_all_bookings():
    response = requests.get(BASE_URL)
    headers_keep_alive = ('Connection', 'keep-alive')
    header_keep_alive = 'Connection'
    assert response.status_code == STATUS_OK
    assert headers_keep_alive in response.headers.items()
    assert header_keep_alive in response.headers


def test_booking_with_id(fixture_payload_with_id):
    response = requests.get(f'{BASE_URL}/{fixture_payload_with_id["bookingid"]}')
    expected_keys = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates']
    for key in expected_keys:
        assert key in response.json().keys()


def test_get_booking_by_id(fixture_payload_with_id):
    response = requests.get(f'{BASE_URL}/{fixture_payload_with_id["bookingid"]}')
    assert response.status_code == STATUS_OK
    assert response.json()['firstname'] == 'Jim'


def test_user_autorization(auth_token):
    response = requests.post(url=AUTH_URL)
    assert response.status_code == STATUS_OK


def test_update_booking(fixture_payload_with_id, auth_token):
    update_payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 222,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"},
        "additionalneeds": "Lunch"
    }
    headers = {'Cookie': f'token={auth_token}'}
    response = requests.put(
        url=f'{BASE_URL}/{fixture_payload_with_id["bookingid"]}', json=update_payload, headers=headers
    )
    assert response.status_code == STATUS_OK
    content = response.json()
    for key in update_payload.keys(): assert update_payload[key] == content[key]


def test_patch_booking(fixture_payload_with_id, auth_token):
    patch_payload = {
        "firstname": "James",
        "lastname": "White"
    }
    headers = {'Cookie': f'token={auth_token}'}
    response = requests.patch(
        url=f'{BASE_URL}/{fixture_payload_with_id["bookingid"]}', json=patch_payload, headers=headers
    )
    assert response.status_code == STATUS_OK
    content = response.json()
    for key in patch_payload.keys(): assert patch_payload[key] == content[key]


def test_delete_booking(fixture_payload_with_id, auth_token):
    headers = {'Cookie': f'token={auth_token}'}
    response = requests.delete(url=f'{BASE_URL}/{fixture_payload_with_id["bookingid"]}', headers=headers)
    assert response.status_code == 201
    response_get = requests.get(f'{BASE_URL}/{fixture_payload_with_id["bookingid"]}')
    assert response_get.status_code == 404  # проверяем, что такого айди больше нет
