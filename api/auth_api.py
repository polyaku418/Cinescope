from custom_requester import CustomRequester
import constants

class AuthAPI(CustomRequester):
    """
      Класс для работы с аутентификацией.
      """

    def __init__(self, session):
        super().__init__(session=session, base_url=constants.BASE_URL)

    def register_user(self, user_data, expected_status=201):

        return self.send_request(
            method='POST',
            endpoint=constants.REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status,
            need_logging=True
        )

    def login_user(self, login_data, expected_status=200):

        return self.send_request(
            method='POST',
            endpoint=constants.LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, user_creds):
        login_data = {
            'email': user_creds[0],
            'password': user_creds[1]
        }

        response = self.login_user(login_data).json
        if 'accessToken' not in response:
            raise KeyError('token is missing')

        token = response['accessToken']
        self._update_session_headers(**{'authorization': 'Bearer' + token})


    def get_auth_token(self, login_data):
        """
        Получаем токен авторизации для пользователя
        """
        response = self.login_user(login_data)
        if 'accessToken' not in response.json():
            raise KeyError('token is missing')
        return response.json()['accessToken']