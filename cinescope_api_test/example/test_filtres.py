import pytest
import logging
logging.getLogger('cinescope_api_test.custom_requester.custom_requester').disabled = True

class TestFiltres:
    # Валидные фильтры
    @pytest.mark.parametrize("minPrice, maxPrice, locations, genreId", [
        (None, None, None, None),
        (100, 500, None, None),
        (None, None, "MSK", None),
        (None, None, None, 1),
        (50, 200, "SPB", None),
    ])

    def test_get_movies_valid_filters(self, minPrice, maxPrice, locations, genreId, api_manager):
        """Тест с валидными фильтрами - должны вернуться фильмы"""
        params = {}
        if minPrice is not None:
            params['minPrice'] = minPrice
        if maxPrice is not None:
            params['maxPrice'] = maxPrice
        if locations is not None:
            params['locations'] = locations
        if genreId is not None:
            params['genreId'] = genreId

        response = api_manager.movie_api.get_movies(params=params, expected_status=200)
        assert 'movies' in response
        assert 'count' in response
        print(f"✅ Найдено {response['count']} фильмов по фильтрам {params}")

    # Пустые результаты (фильтры работают, возвращают 200 с пустым списком)
    @pytest.mark.parametrize("filter_name, filter_value", [
        ("genreId", 999)
    ])

    def test_get_movies_empty_result(self, filter_name, filter_value, api_manager):
        """Тест с фильтрами, которые дают пустой результат (200 OK)"""
        params = {filter_name: filter_value}
        response = api_manager.movie_api.get_movies(params=params, expected_status=200)

        assert response['count'] == 0, f"Ожидался 0, получено {response['count']} фильмов"
        assert len(response['movies']) == 0
        print(f"✅ Пустой результат для {filter_name}={filter_value}")

    # Негативные тесты
    @pytest.mark.parametrize("minPrice, maxPrice, locations, genreId, expected_status", [
        (1000, 500, None, None, 400),  # minPrice > maxPrice
        (-100, 100, None, None, 400),  # Отрицательная цена
        (None, None, "NONEXISTENT", None, 400),  # Несуществующая локация
    ])

    def test_get_movies_invalid_params(self, minPrice, maxPrice, locations, genreId, expected_status, api_manager):
        """Тест с невалидными параметрами
        """
        params = {}
        if minPrice is not None:
            params['minPrice'] = minPrice
        if maxPrice is not None:
            params['maxPrice'] = maxPrice
        if locations is not None:
            params['locations'] = locations
        if genreId is not None:
            params['genreId'] = genreId

        response = api_manager.movie_api.get_movies(params=params, expected_status=expected_status)

        assert 'error' in response or 'message' in response
        print(f"✅ Ошибка {expected_status}: {response.get('message', response.get('error'))}")