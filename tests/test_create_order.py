import pytest
import requests
import allure
from urls import Urls
from data import Data

@allure.feature('Создание заказа')
class TestCreateOrder:

    def _safe_json_parse(self, response):
        
        # Проверяем тип контента
        content_type = response.headers.get('content-type', '').lower()
        if 'application/json' not in content_type:
            print(f"[WARNING] Неверный тип контента: {content_type}. Ответ может быть не JSON.")
            print(f"[DEBUG] Тело ответа (первые 500 символов): {response.text[:500]}")
            return None

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            print(f"[ERROR] Ошибка парсинга JSON: {e}")
            print(f"[DEBUG] Овет: {response.text[:500]}")
            return None


    @allure.title('Создание заказа без авторизации')
    @allure.story('Создание заказа без авторизации')
    def test_create_order_without_authorized(self):
        response = requests.post(Urls.CREATE_ORDER, json=Data.INGREDIENTS)
        response_data = self._safe_json_parse(response)

        assert response.status_code == 401, f"Статус код должен быть 401, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'You should be authorised', \
            f"Сообщение должно быть 'You should be authorised', получено: {response_data.get('message')}"


    @allure.title('Создание заказа с авторизацией')
    @allure.story('Создание заказа с авторизацией и ингредиентами')
    def test_create_order_with_authorizied(self, authorized_user):
        _, access_token = authorized_user

        response = requests.post(Urls.CREATE_ORDER, headers={"Authorization": access_token}, json=Data.INGREDIENTS)
        response_data = self._safe_json_parse(response)

        assert response.status_code == 200, f"Статус код должен быть 200, получен: {response.status_code}"
        assert response_data.get('success') is True, "Поле 'success' должно быть True"
        assert 'order' in response_data, "В ответе должен присутствовать объект order"
        assert 'name' in response_data['order'], "В заказе должен присутствовать name"
        assert 'ingredients' in response_data['order'], "В заказе должен присутствовать ingredients"
        assert 'status' in response_data['order'], "В заказе должен присутствовать status"


    @allure.title('Создание заказа без ингредиентов')
    @allure.story('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, authorized_user):
        _, access_token = authorized_user

        response = requests.post(Urls.CREATE_ORDER, headers={"Authorization": access_token}, json=Data.EMPTY_INGREDIENTS)
        response_data = self._safe_json_parse(response)

        assert response.status_code == 400, f"Статус код должен быть 400, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'Ingredient ids must be provided', \
            f"Сообщение должно быть 'Ingredient ids must be provided', получено: {response_data.get('message')}"

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    @allure.story('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_hash_ingredients(self, authorized_user):
        _, access_token = authorized_user

        response = requests.post(Urls.CREATE_ORDER, headers={"Authorization": access_token}, json=Data.INVALID_HASH_INGREDIENTS)
        response_data = self._safe_json_parse(response)
        
        assert response.status_code == 500, f"Статус код должен быть 500, получен: {response.status_code}"
        
        # Не проверяем поля JSON, если ответ не JSON
        if response_data is not None:
            assert response_data.get('success') is False, "Поле 'success' должно быть False"
            assert 'message' in response_data, "В ответе должно присутствовать сообщение об ошибке"