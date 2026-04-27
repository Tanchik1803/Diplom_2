import pytest
import requests
import allure
from urls import Urls
from data import Data

@allure.feature('Получение заказов пользователя')
class TestGetOrder:

    @allure.title('Получение заказов авторизованным пользователем')
    @allure.story('Получение заказов авторизованным пользователем')
    def test_get_orders_with_authorized(self, authorized_user):
        _, access_token = authorized_user

        # Сначала создаём заказ
        requests.post(Urls.CREATE_ORDER, headers={"Authorization": access_token}, json=Data.INGREDIENTS)

        # Получаем список заказов
        response = requests.get(Urls.GET_ORDERS, headers={"Authorization": access_token})
        response_data = response.json()

        assert response.status_code == 200, f"Статус код должен быть 200, получен: {response.status_code}"
        assert response_data.get('success') is True, "Поле 'success' должно быть True"
        assert 'orders' in response_data, "В ответе должен присутствовать массив orders"
        assert isinstance(response_data['orders'], list), "orders должен быть списком"
        assert len(response_data['orders']) >= 1, "У пользователя должен быть хотя бы один заказ"

    @allure.title('Получение заказов неавторизованным пользователем')
    @allure.story('Получение заказов неавторизованным пользователем')
    def test_get_orders_without_authorized(self):
        response = requests.get(Urls.GET_ORDERS)
        response_data = response.json()

        assert response.status_code == 401, f"Статус код должен быть 401, получен: {response.status_code}"
        assert response_data.get('success') is False, "Поле 'success' должно быть False"
        assert response_data.get('message') == 'You should be authorised', f"Сообщение должно быть 'You should be authorised', получено: {response_data.get('message')}"