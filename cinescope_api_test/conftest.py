import pytest
import requests
from faker import Faker

from cinescope_api_test.clients.api_manager import ApiManager
from cinescope_api_test.utils.data_generator import DataGenerator
from cinescope_api_test.entities.user import User
from cinescope_api_test.entities.roles import Roles
import constants

faker = Faker()

@pytest.fixture(scope='session')
def test_user():
    """
    Генерация случайного пользователя для тестов
    """

    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()
    random_email = DataGenerator.generate_random_email()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
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



@pytest.fixture
def user_session():
    """Фикстура для создания пользовательских сессий"""
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()



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



@pytest.fixture
def super_admin(user_session):
    """Фикстура для работы супер-админа (работа с обычными юзерами)"""
    # Создаем новую сессию через user_session
    new_session = user_session()

    # Получаем данные супер-админа из constants
    admin_email = constants.SUPER_ADMIN['email']
    admin_password = constants.SUPER_ADMIN['password']

    # Авторизуемся как супер-админ
    new_session.auth_api.authenticate((admin_email, admin_password))

    # Создаем объект User
    admin_user = User(
        email=admin_email,
        password=admin_password,
        roles=[Roles.SUPER_ADMIN.value],
        api=new_session
    )

    return admin_user


@pytest.fixture
def common_user(user_session, super_admin):
    """
    Фикстура для создания обычного пользователя с уникальными данными
    """
    new_session = user_session()

    # Генерируем уникальные данные для каждого вызова
    password = DataGenerator.generate_random_password()
    unique_user_data = {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": [Roles.USER.value],
        "verified": True,
        "banned": False
    }

    # Создаем пользователя через супер-админа
    create_response = super_admin.api.user_api.create_user(unique_user_data)
    assert create_response.status_code == 201, "Пользователь не создан"
    user_id = create_response.json()['id']

    # Создаем объект User
    common_user = User(
        email=unique_user_data['email'],
        password=password,
        roles=[Roles.USER.value],
        api=new_session
    )

    # Сохраняем ID пользователя
    common_user.id = user_id

    # Авторизуемся как обычный пользователь
    common_user.api.auth_api.authenticate(common_user.creds)

    return common_user



@pytest.fixture
def authenticated_user(api_manager, registered_user):
    """
    Фикстура для авторизованного обычного пользователя
    """
    login_data = {
        'email': registered_user['email'],
        'password': registered_user['password']
    }

    # Авторизуемся
    response = api_manager.auth_api.login_user(login_data)
    token = response.json()['accessToken']

    # Устанавливаем токен в заголовки
    api_manager.user_api._update_session_headers(authorization=f'Bearer {token}')

    yield api_manager

    # Очистка: удаляем пользователя после тестов
    if 'id' in registered_user:
        api_manager.user_api.delete_user(registered_user['id'])



@pytest.fixture(scope='session')
def movie_api(session):
    """Фикстура для работы с фильмами"""
    from cinescope_api_test.clients.movie_api import MovieAPI
    return MovieAPI(session)

@pytest.fixture(scope="session")
def authenticated_api(api_manager):
    """Фикстура с авторизованной сессией ДЛЯ ФИЛЬМОВ"""
    # Используем SUPER_ADMIN из constants для авторизации
    user_creds = (constants.SUPER_ADMIN['email'], constants.SUPER_ADMIN['password'])
    api_manager.auth_api.authenticate(user_creds)

    def delete_movie(movie_id, expected_status=200):
        """Удалить фильм по ID"""
        return api_manager.movie_api.delete_movie(movie_id, expected_status)
    api_manager.delete_movie = delete_movie
    return api_manager

