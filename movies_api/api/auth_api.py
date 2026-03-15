from .custom_requester import CustomRequester
from . import constants

class AuthAPI(CustomRequester):
    """
      Класс для работы с аутентификацией
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=constants.LOGIN_URL)


    def login_admin(self, login_data, expected_status=200):

        return self.send_request(
            method='POST',
            endpoint=constants.LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )


    def authenticate(self):
        login_data = {
            'email': constants.SUPER_ADMIN['email'],
            'password': constants.SUPER_ADMIN['password']
        }

        response = self.login_admin(login_data).json()
        if 'accessToken' not in response:
            raise KeyError('token is missing')

        token = response['accessToken']
        self._update_session_headers(**{'authorization': 'Bearer ' + token})


    def get_auth_token(self, login_data):
        """
        Получаем токен авторизации
        """
        response = self.login_admin(login_data)
        response_data = response.json()
        print(f"Токен: {response_data.get('accessToken', 'НЕ НАЙДЕН')}")

        if 'accessToken' not in response_data:
            raise KeyError('token is missing')
        return response_data['accessToken']