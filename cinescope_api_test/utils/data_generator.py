import random
import string
from faker import Faker
faker =  Faker()

class DataGenerator:

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{random_string}@ya.ru"

    @staticmethod
    def generate_random_password():
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)
        remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return ''.join(password)

    @staticmethod
    def generate_movie_data():
        """
        Генератор случайных данных для фильма
        """
        # Генерируем случайный идентификатор для фильма (4 символа)
        movie_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
        movie_name = f'Movie {movie_id}'

        # Генерируем цену от 10 до 1000
        price = random.randint(10, 1000)

        # Генерируем описание с использованием movie_id из name
        description = f'Описание тестового фильма \"{movie_name}\"'

        # Случайная локация
        location = random.choice(['SPB', 'MSK'])

        # Случайное значение published (True или False)
        published = random.choice([True, False])

        # Случайный genreId от 1 до 10
        genre_id = random.randint(1, 10)

        # Фиксированный imageUrl
        image_url = 'https://image.url'

        movie_data = {
            'name': movie_name,
            'imageUrl': image_url,
            'price': price,
            'description': description,
            'location': location,
            'published': published,
            'genreId': genre_id
        }

        return movie_data


