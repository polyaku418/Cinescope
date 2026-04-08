from cinescope_api_test.clients.api_manager import ApiManager

class TestGetMoviesApi:
    def test_get_movies_positive(self, api_manager: ApiManager):
        """
        Тест на получение фильмов
        """
        params = {
            'pageSize': 2,
            'page': 1,
            'minPrice': 1,
            'maxPrice': 1000,
            'locations': 'MSK,SPB',
            'published': 'true',
            'createdAt': 'desc',
            'unused_param': None
        }

        response_data = api_manager.movie_api.get_movies(
            params=params,
            expected_status=200
        )

        assert 'movies' in response_data, 'В ответе должно быть поле movies'
        assert 'count' in response_data, 'В ответе должно быть поле count'
        assert 'page' in response_data, 'В ответе должно быть поле page'

        movies = response_data['movies']
        print(f'Получено {len(movies)} фильмов из {response_data["count"]}')

        # Вывести названия фильмов
        for i, movie in enumerate(movies, 1):
            print(f'{i}. {movie["name"]} - {movie["price"]} руб.')


    def test_get_movies_invalid_page_size(self, api_manager: ApiManager):
        """
        Невалидный pageSize
        """

        params = {
            'pageSize': -5,
            'page': 1
        }

        response = api_manager.movie_api.get_movies(
            params=params,
            expected_status=400
        )

        assert 'error' in response or 'message' in response, 'Должно быть сообщение об ошибке'
        print(f'Получена ожидаемая ошибка: {response}')


    def test_get_movies_page_out_of_range(self, api_manager: ApiManager):
        """
        Номер страницы превышает общее количество страниц
        """

        params = {
            "pageSize": 10,
            "page": 9999
        }

        response_data = api_manager.movie_api.get_movies(
            params=params,
            expected_status=200
        )

        if "movies" in response_data:
            movies = response_data["movies"]
            assert len(movies) == 0, f"На странице {params['page']} не должно быть фильмов"
            print(f"Корректно: на странице {params['page']} нет фильмов")
        else:
            print(f"Ответ без поля movies: {response_data}")
