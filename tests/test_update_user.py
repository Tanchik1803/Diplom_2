import pytest
import requests
import allure
from urls import Urls
from data import Data

@allure.feature('Обновление данных пользователя')
class TestUpdateUser:

    @allure.title('Обновление email авторизованным пользователем')
    @allure.story('Изменение данных с авторизацией - поле email')
    def test_update_with_authorized_email(self, authorized_user):
        _, access_token = authorized_user

        response = requests.patch(Urls.USER_UPDATE, headers={'Authorization': access_token}, json=Data.UPDATE_EMAIL)
        response_data = response.json()

        assert response.status_code == 200, f"Статус код должен быть 200, получен: {response.status_code}"
        assert response_data.get('success') is True, "Поле 'success' должно быть True"
        assert response_data['user']['email'] == Data.UPDATE_EMAIL['email'], \
            f"Email должен быть обновлён: {response_data['user']['email']} != {Data.UPDATE_EMAIL['email']}"

        # Очистка
        requests.delete(Urls.USER_DELETE, headers={'Authorization': access_token})

    @allure.title('Обновление имени авторизованным пользователем')
    @allure.story('Изменение данных с авторизацией - поле name')
    def test_update_with_authorized_name(self, authorized_user):
        _, access_token = authorized_user

        response = requests.patch(Urls.USER_UPDATE, headers={'Authorization': access_token}, json=Data.UPDATE_NAME)
        response_data = response.json()

        assert response.status_code == 200, f"Статус код должен быть 200, получен: {response.status_code}"
        assert response_data.get('success') is True, "Поле 'success' должно быть True"
        assert response_data['user']['name'] == Data.UPDATE_NAME['name'], \
            f"Имя должно быть обновлено: {response_data['user']['name']} != {Data.UPDATE_NAME['name']}"

        # Очистка
        requests.delete(Urls.USER_DELETE, headers={'Authorization': access_token})

    @allure.title('Обновление пароля авторизованным пользователем')
    @allure.story('Изменение данных с авторизацией - поле password')
    def test_update_with_authorized_password(self, authorized_user):
        _, access_token = authorized_user

        response = requests.patch(Urls.USER_UPDATE, headers={'Authorization': access_token}, json=Data.UPDATE_PASSWORD)
        response_data = response.json()

        assert response.status_code == 200, f"Статус код должен быть 200, получен: {response.status_code}"
        assert response_data.get('success') is True, "Поле 'success' должно быть True"
        assert 'user' in response_data, "В ответе должен присутствовать объект user"

        # Очистка
        requests.delete(Urls.USER_DELETE, headers={'Authorization': access_token})

    @allure.title('Обновление email без авторизации')
    @allure.story('Изменение данных без авторизации - поле email')
    def test_update_email_without_authorized(self):
        response = requests.patch(Urls.USER_UPDATE, json=Data.UPDATE_EMAIL)
        response_data = response.json()

        assert response.status_code == 401, f"Статус код должен быть 401, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'You should be authorised', \
            f"Сообщение должно быть 'You should be authorised', получено: {response_data.get('message')}"

    @allure.title('Обновление имени без авторизации')
    @allure.story('Изменение данных без авторизации - поле name')
    def test_update_name_without_authorized(self):
        response = requests.patch(Urls.USER_UPDATE, json=Data.UPDATE_NAME)
        response_data = response.json()

        assert response.status_code == 401, f"Статус код должен быть 401, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'You should be authorised', \
            f"Сообщение должно быть 'You should be authorised', получено: {response_data.get('message')}"

    @allure.title('Обновление пароля без авторизации')
    @allure.story('Изменение данных без авторизации - поле password')
    def test_update_password_without_authorized(self):
        response = requests.patch(Urls.USER_UPDATE, json=Data.UPDATE_PASSWORD)
        response_data = response.json()

        assert response.status_code == 401, f"Статус код должен быть 401, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'You should be authorised', \
            f"Сообщение должно быть 'You should be authorised', получено: {response_data.get('message')}"