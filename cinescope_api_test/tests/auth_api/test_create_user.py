from cinescope_api_test.utils.data_generator import DataGenerator
import pytest

class TestUser:
    def test_create_user(self, super_admin):
        """
        Тест на создание пользователя через user_api.create_user
        """
        # Генерируем уникальные данные для этого теста, чтобы избежать конфликтов
        unique_user_data = {
            "email": DataGenerator.generate_random_email(),
            "fullName": DataGenerator.generate_random_name(),
            "password": DataGenerator.generate_random_password(),
            "passwordRepeat": DataGenerator.generate_random_password(),
            "roles": ["USER"],
            "verified": True,
            "banned": False
        }

        # Важно: password и passwordRepeat должны совпадать
        password = DataGenerator.generate_random_password()
        unique_user_data["password"] = password
        unique_user_data["passwordRepeat"] = password

        response = super_admin.api.user_api.create_user(unique_user_data).json()
        user_id = response['id']

        assert response.get('id') and response['id'] != '', "ID должен быть не пустым"
        assert response.get('email') == unique_user_data['email']
        assert response.get('fullName') == unique_user_data['fullName']
        assert response.get('roles', []) == unique_user_data['roles']
        assert response.get('verified') is True

        print(f'✅ Создан пользователь: {response["email"]} (ID: {response["id"]})')

        # Удаляем после теста
        super_admin.api.user_api.delete_user(user_id)

    def test_get_user_by_locator(self, super_admin):
        """
        Тест на получение пользователя по ID и email через супер-админа
        """
        # Генерируем уникальные данные для этого теста
        password = DataGenerator.generate_random_password()
        unique_user_data = {
            "email": DataGenerator.generate_random_email(),
            "fullName": DataGenerator.generate_random_name(),
            "password": password,
            "passwordRepeat": password,
            "roles": ["USER"],
            "verified": True,
            "banned": False
        }

        # 1. Создаем пользователя
        created_user_response = super_admin.api.user_api.create_user(unique_user_data).json()
        user_id = created_user_response['id']
        user_email = created_user_response['email']

        print(f'📝 Создан тестовый пользователь: {user_email} (ID: {user_id})')

        # 2. Получаем пользователя по ID
        response_by_id = super_admin.api.user_api.get_user_info(user_id).json()

        # 3. Проверяем данные
        assert response_by_id.get('id') and response_by_id['id'] != '', "ID должен быть не пустым"
        assert response_by_id.get('email') == unique_user_data['email']
        assert response_by_id.get('fullName') == unique_user_data['fullName']
        assert response_by_id.get('roles', []) == unique_user_data['roles']
        assert response_by_id.get('verified') is True

        print(f'✅ Пользователь {user_id} успешно найден по ID')

        # Удаляем после теста
        super_admin.api.user_api.delete_user(user_id)

    def test_get_user_by_id_common_user(self, common_user):
        """
        Негативный тест: USER не может получить информацию о пользователе
        """
        with pytest.raises(Exception) as exc_info:
            common_user.api.user_api.get_user_info(common_user.email)

        assert any(code in str(exc_info.value) for code in ['403', '401']), \
            f"Ожидалась ошибка 403/401, получена: {exc_info.value}"

        print('✅ Доступ запрещен для USER')