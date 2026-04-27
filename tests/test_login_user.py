import pytest
import requests
import allure
from urls import Urls

@allure.feature('Авторизация пользователя')
class TestLoginUser:

    @allure.title('Успешный логин существующего пользователя')
    @allure.story('Логин под существующим пользователем')
    def test_login_success_user(self, create_user):
        user_data, _, _ = create_user

        response = requests.post(Urls.USER_LOGIN, json=user_data)
        response_data = response.json()

        assert response.status_code == 200, f"Статус код должен быть 200, получен: {response.status_code}"
        assert response_data.get('success') is True, "Поле 'success' должно быть True"
        assert 'accessToken' in response_data, "В ответе должен присутствовать accessToken"
        assert 'refreshToken' in response_data, "В ответе должен присутствовать refreshToken"
        assert 'user' in response_data, "В ответе должен присутствовать объект user"
        assert response_data['user']['email'] == user_data['email'], \
            f"Email должен совпадать: {response_data['user']['email']} != {user_data['email']}"
        assert response_data['user']['name'] == user_data['name'], \
            f"Имя должно совпадать: {response_data['user']['name']} != {user_data['name']}"

    @allure.title('Логин с неверным email')
    @allure.story('Логин с неверным логином')
    def test_login_incorrect_email(self, create_user):
        user_data, _, _ = create_user

        login_data = {
            "email": "nonexistent@example.com",
            "password": user_data["password"]
        }

        response = requests.post(Urls.USER_LOGIN, json=login_data)
        response_data = response.json()

        assert response.status_code == 401, f"Статус код должен быть 401, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'email or password are incorrect', \
            f"Сообщение должно быть 'email or password are incorrect', получено: {response_data.get('message')}"

    @allure.title('Логин с неверным паролем')
    @allure.story('Логин с неверным паролем')
    def test_login_incorrect_password(self, create_user):
        user_data, _, _ = create_user

        login_data = {
            "email": user_data["email"],
            "password": "wrongpassword123"
        }

        response = requests.post(Urls.USER_LOGIN, json=login_data)
        response_data = response.json()

        assert response.status_code == 401, f"Статус код должен быть 401, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'email or password are incorrect', \
            f"Сообщение должно быть 'email or password are incorrect', получено: {response_data.get('message')}"