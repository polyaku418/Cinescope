from movies_api.custom_requester import CustomRequester
from movies_api import constants
import urllib.parse

class MovieAPI(CustomRequester):
    """
      Класс для работы с фильмами
    """

    def __init__(self, session):
        super().__init__(session=session, base_url=constants.MOVIES_URL)

    # тут получаем всю афишу, не фильм
    def get_movies(self, params=None, expected_status=200):

        endpoint = constants.MOVIES_ENDPOINT

        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            if filtered_params:
                query_string = urllib.parse.urlencode(filtered_params)
                endpoint = f'{endpoint}?{query_string}'

        response = self.send_request(
            method='GET',
            endpoint=endpoint,
            expected_status=expected_status
        )

        if response.status_code == expected_status:
            return response.json()
        return response

    # создаем фильм
    def post_movies(self, data=None, expected_status=201):

        response = self.send_request(
            method='POST',
            endpoint=constants.MOVIES_ENDPOINT,
            data=data,
            expected_status=expected_status
        )

        if response.status_code == expected_status:
            return response.json()
        return response

    # получаем созданный фильм
    def get_movie_by_id(self, movie_id, expected_status=200):

        endpoint = f"{constants.MOVIES_ENDPOINT}/{movie_id}"

        response = self.send_request(
            method='GET',
            endpoint=endpoint,
            expected_status=expected_status
        )

        if response.status_code == expected_status:
            return response.json()
        return response

    # обновление полей фильма
    def patch_movie(self, movie_id, data=None, expected_status=200):

        endpoint = f"{constants.MOVIES_ENDPOINT}/{movie_id}"

        response = self.send_request(
            method='PATCH',
            endpoint=endpoint,
            data=data,
            expected_status=expected_status
        )

        if response.status_code == expected_status:
            return response.json()
        return response

    # удаляем фильмы, в тч после тестов
    def delete_movie(self, movie_id, expected_status=200):
        """
        Удаление фильма по ID
        """
        endpoint = f"{constants.MOVIES_ENDPOINT}/{movie_id}"

        response = self.send_request(
            method='DELETE',
            endpoint=endpoint,
            expected_status=expected_status
        )
        # доп проверка
        # if response.status_code == expected_status:
        #     try:
        #         return response.json()
        #     except:
        #         return response
        return response