from auth_api import AuthAPI
from user_api import UserApi

# центральный класс для управления всеми API-классами.
class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserApi(session)