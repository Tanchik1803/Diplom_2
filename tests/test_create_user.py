import pytest
import requests
import allure
from urls import Urls

@allure.feature('Регистрация пользователя')
class TestCreateUser:

    @allure.title('Успешная регистрация нового пользователя')
    @allure.story('Создание уникального пользователя')
    def test_create_unique_user(self, generate_user_data):
        response = requests.post(Urls.CREATE_USER, json=generate_user_data)
        response_data = response.json()

        assert response.status_code == 200, f"Статус код должен быть 200, получен: {response.status_code}"
        assert response_data.get('success') is True, "Поле 'success' должно быть True"
        assert 'accessToken' in response_data, "В ответе должен присутствовать accessToken"
        assert 'refreshToken' in response_data, "В ответе должен присутствовать refreshToken"
        assert 'user' in response_data, "В ответе должен присутствовать объект user"
        assert response_data['user']['email'] == generate_user_data['email'], "Email в ответе должен совпадать с отправленным"
        assert response_data['user']['name'] == generate_user_data['name'], "Имя в ответе должно совпадать с отправленным"

        # Очистка
        requests.delete(Urls.USER_DELETE, headers={'Authorization': response_data['accessToken']})

    @allure.title('Регистрация уже существующего пользователя')
    @allure.story('Создание пользователя, который уже зарегистрирован')
    def test_create_existing_user(self, create_user):
        user_data, _, _ = create_user

        response = requests.post(Urls.CREATE_USER, json=user_data)
        response_data = response.json()

        assert response.status_code == 403, f"Статус код должен быть 403, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'User already exists', \
            f"Сообщение должно быть 'User already exists', получено: {response_data.get('message')}"

    @allure.title('Регистрация без обязательных полей')
    @allure.story('Создание пользователя без обязательных полей')
    @pytest.mark.parametrize("test_data, expected_message", [
        ({"email": "", "password": "qwerty123", "name": "Test"}, "Email, password and name are required fields"),
        ({"email": "test@example.com", "password": "", "name": "Test"}, "Email, password and name are required fields"),
        ({"email": "test@example.com", "password": "qwerty123", "name": ""}, "Email, password and name are required fields"),
        ({"password": "qwerty123", "name": "Test"}, "Email, password and name are required fields"),
        ({"email": "test@example.com", "name": "Test"}, "Email, password and name are required fields"),
        ({"email": "test@example.com", "password": "qwerty123"}, "Email, password and name are required fields"),
    ])
    def test_create_user_without_required_fields(self, test_data, expected_message):
        response = requests.post(Urls.CREATE_USER, json=test_data)
        response_data = response.json()

        assert response.status_code == 403, f"Статус код должен быть 403, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == expected_message, \
            f"Сообщение должно быть '{expected_message}', получено: {response_data.get('message')}"