from .api_manager import ApiManager
from .constants import SUPER_ADMIN

class TestAuthApi:
    def test_login_user(self, api_manager: ApiManager):
        """
        Тест на авторизацию пользователя
        """
        login_data = {
            'email': SUPER_ADMIN['email'],
            'password': SUPER_ADMIN['password']
        }
        response = api_manager.auth_api.login_admin(login_data)
        response_data = response.json()

        assert 'accessToken' in response_data, 'Токен доступа отсутствует в ответе'
        assert response.status_code== 200, 'Статус код не совпадает'