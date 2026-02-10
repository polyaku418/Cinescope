from api_manager import ApiManager

class TestAuthApi:
    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()

        assert response_data['email'] == test_user['email'], 'Email не совпадает'
        assert 'id' in response_data, 'ID пользователя отсутствует в ответе'
        assert 'roles' in response_data, 'Роли пользователя отсутствуют в ответе'
        assert 'USER' in response_data['roles'], 'Роль USER должна быть у пользователя'

        user_id = response_data['id']
        login_data = {
            'email': test_user['email'],
            'password': test_user['password']
        }
        login_response = api_manager.auth_api.login_user(login_data)
        token = login_response.json()['accessToken']
        api_manager.user_api._update_session_headers(
            authorization=f'Bearer {token}'
        )
        api_manager.user_api.delete_user(user_id)

    def test_register_and_login_user(self, api_manager: ApiManager, registered_user):
        """
        Тест на регистрацию и авторизацию пользователя
        """
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        response = api_manager.auth_api.login_user(login_data)
        response_data = response.json()

        assert 'accessToken' in response_data, 'Токен доступа отсутствует в ответе'
        assert response_data['user']['email'] == registered_user['email'], 'Email не совпадает'


        # УДАЛЕНИЕ ПОСЛЕ ТЕСТА
        if 'id' in registered_user:
            # Получаем токен
            token = response_data['accessToken']
            # Устанавливаем заголовок авторизации
            api_manager.user_api._update_session_headers(
                authorization=f'Bearer {token}'
            )
            # Удаляем пользователя
            api_manager.user_api.delete_user(registered_user['id'])