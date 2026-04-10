import os
from dotenv import load_dotenv

load_dotenv()


BASE_URL = 'https://auth.dev-cinescope.coconutqa.ru/'
LOGIN_URL = 'https://auth.dev-cinescope.coconutqa.ru/'

LOGIN_ENDPOINT = '/login'
REGISTER_ENDPOINT = '/register'

MOVIES_URL = 'https://api.dev-cinescope.coconutqa.ru/'
MOVIES_ENDPOINT = '/movies'

HEADERS = {
    'content-type': 'application/json',
    'accept': 'application/json'
}

SUPER_ADMIN = {
    'email': os.getenv('SUPER_ADMIN_EMAIL'),
    'password': os.getenv('SUPER_ADMIN_PASSWORD')
}