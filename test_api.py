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
def booking_id():
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
    booking_id = response.json()['bookingid']
    yield booking_id


def test_get_all_bookings():
    response = requests.get(BASE_URL)
    headers_keep_alive = ('Connection', 'keep-alive')
    header_keep_alive = 'Connection'
    assert response.status_code == STATUS_OK
    assert headers_keep_alive in response.headers.items()
    assert header_keep_alive in response.headers


def test_booking_with_id():
    response = requests.get(f"{BASE_URL}/1")
    response.data = response.json()
    expected_keys = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates']
    for key in expected_keys:
        assert key in response.data.keys()


def test_create_booking(booking_id):  # передаем фикстуру в функцию
    response = requests.get(f'{BASE_URL}/{booking_id}')
    assert response.status_code == STATUS_OK
    assert response.json()['firstname'] == 'Jim'


def test_user_autorization(auth_token):
    response = requests.post(url=AUTH_URL)
    assert response.status_code == STATUS_OK


def test_update_booking(booking_id, auth_token):
    payload = {
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
    response = requests.put(url=f'{BASE_URL}/{booking_id}', json=payload, headers=headers)
    assert response.status_code == STATUS_OK
    assert response.json()['totalprice'] == payload['totalprice']
    assert response.json()['additionalneeds'] == payload['additionalneeds']


def test_delete_booking(booking_id, auth_token):
    headers = {'Cookie': f'token={auth_token}'}
    response = requests.delete(url=f'{BASE_URL}/{booking_id}', headers=headers)
    assert response.status_code == 201
    response_get = requests.get(f'{BASE_URL}/{booking_id}')
    assert response_get.status_code == 404  # проверяем, что такого айди больше нет

def test_patch_booking(booking_id, auth_token):
    payload = {
        "firstname": "James",
        "lastname": "White"
    }
    headers = {'Cookie': f'token={auth_token}'}
    response = requests.patch(url=f'{BASE_URL}/{booking_id}', json=payload, headers=headers)
    assert response.json()['firstname'] == payload['firstname']
    assert response.json()['lastname'] == payload['lastname']

