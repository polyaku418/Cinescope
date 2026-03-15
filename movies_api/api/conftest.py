import pytest
import requests

from movies_api.api.api_manager import ApiManager

@pytest.fixture(scope='session')
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope='session')
def api_manager(session):
    return ApiManager(session)

@pytest.fixture(scope="session")
def authenticated_api(api_manager):
    """Фикстура с авторизованной сессией"""
    api_manager.auth_api.authenticate()

    def delete_movie(movie_id, expected_status=200):
        """Удалить фильм по ID"""
        return api_manager.movie_api.delete_movie(movie_id, expected_status)
    api_manager.delete_movie = delete_movie
    return api_manager

@pytest.fixture(scope='session')
def movie_api(session):
    """Фикстура для работы с фильмами"""
    from movies_api.api.movie_api import MovieAPI
    return MovieAPI(session)

