import pytest
import requests
from faker import Faker

from api_manager import ApiManager
from data_generator import DataGenerator

faker = Faker()

@pytest.fixture(scope='session')
def test_user():
    """
    Генерация случайного пользователя для тестов.
    Добавляем временную метку для уникальности.
    """

    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()
    random_email = DataGenerator.generate_random_email()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }
@pytest.fixture(scope='session')
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user)
    user_data = response.json()
    registered_user = {**test_user, **user_data}
    return registered_user

@pytest.fixture(scope='session')
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope='session')
def api_manager(session):
    return ApiManager(session)

