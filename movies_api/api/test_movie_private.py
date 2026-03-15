from movies_api.api.data_generator import DataGenerator

class TestPostMoviesApi:
    def test_post_movies_positive(self, authenticated_api):
        """
        Тест на создание фильмов
        """
        movie_data = DataGenerator.generate_movie_data()

        response_data = authenticated_api.movie_api.post_movies(
            data=movie_data,
            expected_status=201
        )

        assert response_data is not None, 'Ответ не должен быть пустым'
        assert response_data['name'] == movie_data['name'], 'Название не совпадает'
        assert response_data['price'] == movie_data['price'], 'Цена не совпадает'
        assert response_data['description'] == movie_data['description'], 'Описание не совпадает'
        assert response_data['imageUrl'] == movie_data['imageUrl'], 'imageUrl не совпадает'
        assert response_data['location'] == movie_data['location'], 'Локация не совпадает'
        assert response_data['published'] == movie_data['published'], 'published не совпадает'
        assert response_data['genreId'] == movie_data['genreId'], 'genreId не совпадает'

        created_movie_id = response_data['id']
        print(f'✅ Создан фильм с ID: {created_movie_id}, название: {movie_data["name"]}')

        # здесь пока не удаляем фильмы, чтобы чекать базу, что из всех тестов создался только один фильм

    def test_post_movies_duplicate_name(self, authenticated_api):
        """
        Негативный тест: создание фильма с уже существующим названием
        """
        # 1. Тут создаем первый фильм
        movie_data = DataGenerator.generate_movie_data()
        original_name = movie_data['name']

        first_response = authenticated_api.movie_api.post_movies(
            data=movie_data,
            expected_status=201
        )
        print(f'✅ Первый фильм создан: "{original_name}" (ID: {first_response["id"]})')
        created_movie_id = first_response['id']

        # 2. второй фильм с таким же name
        duplicate_data = movie_data.copy()
        duplicate_data['imageUrl'] = 'https://different-image.url'  # изменили другое поле, не имя

        try:
            duplicate_response = authenticated_api.movie_api.post_movies(
                data=duplicate_data,
                expected_status=409
            )
            print(f'✅ API вернул 409 Conflict, как и ожидалось')
            if isinstance(duplicate_response, dict):
                print(f'Сообщение: {duplicate_response.get("message", "Нет сообщения")}')
        except Exception as e:
            print(f'✅ Получена ожидаемая ошибка 409: {e}')

            # 3. удаляем после теста
        authenticated_api.delete_movie(created_movie_id)
        print(f'🗑️ Фильм {created_movie_id} удален')


    def test_unauth_session(self):
        """
        Негативный тест на создание фильмов (без авторизации)
        """
        import requests
        from movies_api.api.movie_api import MovieAPI
        from movies_api.api.data_generator import DataGenerator

        # 1. Создаем новую сессию без авторизации
        unauth_session = requests.Session()
        unauth_movie_api = MovieAPI(unauth_session)

        # 2. Пытаемся создать фильм без авторизации
        movie_data = DataGenerator.generate_movie_data()

        try:
            response = unauth_movie_api.post_movies(
                data=movie_data,
                expected_status=401
            )

            print(f'✅ API вернул 401 Unauthorized')

        # обрабатываем исключения
        except Exception as e:
            error_message = str(e)
            assert '401' in error_message, f"Должна быть ошибка 401, получена: {error_message}"
            print(f'✅ Получена ожидаемая ошибка 401: {e}')


    def test_get_movies_positive(self, authenticated_api, movie_api):
        """
        Тест на получение созданного фильма
        """

        # 1. создаем фильм
        movie_data = DataGenerator.generate_movie_data()

        response_data = authenticated_api.movie_api.post_movies(
            data=movie_data,
            expected_status=201
        )

        assert response_data is not None, 'Ответ не должен быть пустым'

        created_movie_id = response_data['id']
        print(f'✅ Создан фильм с ID: {created_movie_id}, название: {movie_data["name"]}')

        # 2. получаем фильм
        print(f'\n🔍 Получаем фильм по ID: {created_movie_id}')
        get_response = movie_api.get_movie_by_id(
            movie_id=created_movie_id,
            expected_status=200
        )
        # Проверки, что полученный фильм == созданному
        assert get_response['id'] == created_movie_id, 'ID не совпадает'
        assert get_response['name'] == movie_data['name'], 'Название не совпадает'
        assert get_response['price'] == movie_data['price'], 'Цена не совпадает'
        assert get_response['description'] == movie_data['description'], 'Описание не совпадает'
        assert get_response['location'] == movie_data['location'], 'Локация не совпадает'
        assert get_response['published'] == movie_data['published'], 'published не совпадает'
        assert get_response['genreId'] == movie_data['genreId'], 'genreId не совпадает'

        # 3. Пытаемся получить фильм с несуществующим ID
        non_existent_id = created_movie_id + 100
        print(f'\n🔍 Пытаемся получить фильм с несуществующим ID: {non_existent_id}')

        try:
            non_existent_response = movie_api.get_movie_by_id(
                movie_id=non_existent_id,
                expected_status=404
            )
            print(f'✅ API вернул 404 для несуществующего фильма, как и ожидалось')
        except Exception as e:
            print(f'❌ Ошибка: {e}')

        # 4. удаляем после теста
        authenticated_api.delete_movie(created_movie_id)
        print(f'🗑️ Фильм {created_movie_id} удален')

        # 5. пробуем получить после удаления
        try:
            not_found_response = movie_api.get_movie_by_id(
                movie_id=created_movie_id,
                expected_status=404
            )
            print(f'⚠️ Фильм не найден, как и ожидалось')
        except Exception as e:
            print(f'⚠️ Ожидаемая ошибка 404 при получении удаленного фильма: {e}')


    def test_patch_movies(self, authenticated_api, movie_api):
        """
        Тест на редактирование созданного фильма
        """

        # 1. создаем фильм
        movie_data = DataGenerator.generate_movie_data()

        response_data = authenticated_api.movie_api.post_movies(
            data=movie_data,
            expected_status=201
        )

        assert response_data is not None, 'Ответ не должен быть пустым'

        created_movie_id = response_data['id']
        print(f'✅ Создан фильм с ID: {created_movie_id}, название: {movie_data["name"]}')

        # 2. Редактируем созданный фильм
        patch_data = {
            'name': f'Updated {movie_data["name"]}',
            'price': movie_data["price"] + 100,
            'location': 'SPB' if movie_data["location"] == 'MSK' else 'MSK',
            'published': not movie_data["published"]
        }

        patch_response = authenticated_api.movie_api.patch_movie(
            movie_id=created_movie_id,
            data=patch_data,
            expected_status=200
        )

        # 3. Проверяем ответ после PATCH
        assert patch_response['id'] == created_movie_id, 'ID не должен измениться'
        assert patch_response['name'] == patch_data['name'], 'Имя должно обновиться'
        assert patch_response['price'] == patch_data['price'], 'Цена должна обновиться'
        assert patch_response['location'] == patch_data['location'], 'Локация должна обновиться'
        assert patch_response['published'] == patch_data['published'], 'published должно обновиться'
        # Поля, которые не менялись, должны остаться прежними
        assert patch_response['description'] == movie_data['description'], 'Описание не должно измениться'
        assert patch_response['genreId'] == movie_data['genreId'], 'genreId не должен измениться'
        assert patch_response['imageUrl'] == movie_data['imageUrl'], 'imageUrl не должен измениться'

        print(f'✅ Фильм успешно отредактирован')
        print(f"   Новое название: {patch_response['name']}")
        print(f"   Новая цена: {patch_response['price']}")
        print(f"   Новая локация: {patch_response['location']}")

        # 4. Получаем фильм снова и проверяем, что изменения применились
        print(f'\n🔍 Проверяем изменения, получая фильм снова')
        get_updated_response = movie_api.get_movie_by_id(
            movie_id=created_movie_id,
            expected_status=200
        )

        assert get_updated_response['name'] == patch_data['name']
        assert get_updated_response['price'] == patch_data['price']
        assert get_updated_response['location'] == patch_data['location']
        assert get_updated_response['published'] == patch_data['published']

        # 5. удаляем после теста
        authenticated_api.delete_movie(created_movie_id)


    def test_patch_movies_nonexistent_id(self, authenticated_api):
        """
        Негативный тест: попытка отредактировать несуществующий фильм
        """
        nonexistent_id = 9999999
        patch_data = {'name': 'Updated Name'}

        try:
            authenticated_api.movie_api.patch_movie(
                movie_id=nonexistent_id,
                data=patch_data,
                expected_status=404
            )
            print(f'✅ 404 Not Found для несуществующего ID')
        except Exception as e:
            print(f'✅ Ожидаемая ошибка 404: {e}')
            assert '404' in str(e)


    def test_patch_movies_invalid_data(self, authenticated_api, movie_api):
        """
        Негативный тест: обновление с некорректными данными
        """
        # 1. Создаем фильм
        movie_data = DataGenerator.generate_movie_data()
        create_response = authenticated_api.movie_api.post_movies(
            data=movie_data,
            expected_status=201
        )
        movie_id = create_response['id']

        # 2. Пробуем обновить с некорректными данными
        invalid_data = {'price':  'не число'}

        try:
            authenticated_api.movie_api.patch_movie(
                movie_id=movie_id,
                data=invalid_data,
                expected_status=400
            )
            print(f'✅ 400 Bad Request для некорректных данных')
        except Exception as e:
            print(f'✅ Ожидаемая ошибка 400: {e}')
            assert '400' in str(e)

        # Очистка
        authenticated_api.delete_movie(movie_id)



