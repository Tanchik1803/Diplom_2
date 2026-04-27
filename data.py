from faker import Faker

fake = Faker()

class Data:
    """Тестовые данные для API тестов"""

    # Обновление данных пользователя
    UPDATE_EMAIL = {'email': fake.email()}
    UPDATE_NAME = {'name': fake.name()}
    UPDATE_PASSWORD = {'password': fake.password(length=10)}

    # Ингредиенты для заказа
    INGREDIENTS = {
        "ingredients": ["61c0c5a71d1f82001bdaaa77", "61c0c5a71d1f82001bdaaa6d"]
    }

    INVALID_HASH_INGREDIENTS = {
        "ingredients": ["invalid_hash_123"]
    }

    EMPTY_INGREDIENTS = {
        "ingredients": []
    }

    # Данные для логина с неверными данными
    INVALID_LOGIN = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }