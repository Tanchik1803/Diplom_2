import pytest
import requests
from faker import Faker
from urls import Urls

fake = Faker()

@pytest.fixture
def generate_user_data():
    """Генерирует уникальные данные пользователя для каждого теста"""
    return {
        "email": fake.email(),
        "password": fake.password(length=8),
        "name": fake.name()
    }

@pytest.fixture
def create_user(generate_user_data):
    """Создаёт пользователя и возвращает данные + токен. Удаляет пользователя после теста."""
    response = requests.post(Urls.CREATE_USER, json=generate_user_data)
    response_data = response.json()

    yield generate_user_data, response_data, response.status_code

    # Очистка: удаляем созданного пользователя
    access_token = response_data.get('accessToken')
    if access_token:
        requests.delete(Urls.USER_DELETE, headers={'Authorization': access_token})

@pytest.fixture
def authorized_user(create_user):
    """Возвращает авторизованного пользователя с access_token"""
    user_data, response_data, status_code = create_user
    access_token = response_data.get('accessToken')
    return user_data, access_token