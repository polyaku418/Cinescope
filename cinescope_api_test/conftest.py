import pytest
import requests
from faker import Faker

from cinescope_api_test.clients.api_manager import ApiManager
from cinescope_api_test.utils.data_generator import DataGenerator
import constants

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

@pytest.fixture(scope='function')
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        'verified': True,
        'banned': False
    })
    return updated_data

@pytest.fixture(scope="session")
def authenticated_api(api_manager):
    """Фикстура с авторизованной сессией"""
    # Используем SUPER_ADMIN из constants для авторизации
    user_creds = (constants.SUPER_ADMIN['email'], constants.SUPER_ADMIN['password'])
    api_manager.auth_api.authenticate(user_creds)

    def delete_movie(movie_id, expected_status=200):
        """Удалить фильм по ID"""
        return api_manager.movie_api.delete_movie(movie_id, expected_status)
    api_manager.delete_movie = delete_movie
    return api_manager

@pytest.fixture(scope='session')
def movie_api(session):
    """Фикстура для работы с фильмами"""
    from cinescope_api_test.clients.movie_api import MovieAPI
    return MovieAPI(session)
