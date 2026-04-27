class Urls:
    """URL-адреса эндпоинтов API Stellar Burgers"""

    BASE_URL = 'https://stellarburgers.education-services.ru'

    # Авторизация и пользователи
    CREATE_USER = f'{BASE_URL}/api/auth/register'
    USER_LOGIN = f'{BASE_URL}/api/auth/login'
    USER_UPDATE = f'{BASE_URL}/api/auth/user'
    USER_DELETE = f'{BASE_URL}/api/auth/user'

    # Заказы
    CREATE_ORDER = f'{BASE_URL}/api/orders'
    GET_ORDERS = f'{BASE_URL}/api/orders'