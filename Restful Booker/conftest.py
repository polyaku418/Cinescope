import pytest
import requests
from faker import Faker
from constants import HEADERS, BASE_URL

faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"{BASE_URL}/auth",
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    session.headers.update({"Accept": "application/json"})
    return session

@pytest.fixture
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }

@pytest.fixture
def updated_booking_data(booking_data):
    return {
        "firstname": "UPDATED_" + booking_data["firstname"],
        "lastname": booking_data["lastname"],
        "totalprice": booking_data["totalprice"] + 100,
        "depositpaid": not booking_data["depositpaid"],
        "bookingdates": {
            "checkin": "2024-05-10",
            "checkout": "2024-05-15"
        },
        "additionalneeds": "Breakfast"
    }

@pytest.fixture
def updated_patch_booking_data(booking_data):
    return {
    "firstname": "UpdatedName",
    "totalprice": 250
}