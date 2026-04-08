from cinescope_api_test.clients.auth_api import AuthAPI
from cinescope_api_test.clients.user_api import UserApi
from cinescope_api_test.clients.movie_api import MovieAPI

# центральный класс для управления всеми API-классами.
class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserApi(session)
        self.movie_api = MovieAPI(session)

    def close_session(self):
        self.session.close()