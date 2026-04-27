import requests
from typing import Optional, Dict, Any

class APIHelpers:
    """Вспомогательные методы для работы с API"""

    @staticmethod
    def safe_json_parse(response: requests.Response) -> Optional[Dict[str, Any]]:
        """Безопасный парсинг JSON ответа"""
        try:
            return response.json()
        except ValueError:
            return None