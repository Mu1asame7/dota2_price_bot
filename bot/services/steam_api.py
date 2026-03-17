# bot/services/steam_api.py
import requests
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# ID игры Dota 2 в Steam
DOTA_2_APP_ID = 570


class SteamAPI:
    """Класс для работы с Steam API"""

    BASE_URL = "https://steamcommunity.com/market"

    @classmethod
    def get_item_price(cls, item_name: str) -> Optional[Dict[str, Any]]:
        """
        Получает информацию о цене предмета с Steam Market.

        Args:
            item_name: Название предмета (например, "Arcana of the Fiend")

        Returns:
            Словарь с информацией о цене или None, если предмет не найден
        """
        url = f"{cls.BASE_URL}/priceoverview/"
        params = {
            "appid": DOTA_2_APP_ID,
            "currency": 1,  # 1 = USD, 5 = RUB
            "market_hash_name": item_name
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logger.warning(f"Предмет '{item_name}' не найден на Steam Market")
                return None

            return {
                "name": item_name,
                "lowest_price": data.get("lowest_price"),
                "median_price": data.get("median_price"),
                "volume": data.get("volume"),
                "success": True
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при запросе к Steam API: {e}")
            return None

@classmethod
def search_items(cls, search_term: str, max_results: int = 10) -> Optional[list]:
    """
    Ищет предметы по названию.
    
    Параметры:
        search_term: Поисковый запрос
        max_results: Максимальное количество результатов
    
    Возвращает:
        Список найденных предметов или None
    """
    url = f"{cls.BASE_URL}/search/render/"
    params = {
        "query": search_term,
        "start": 0,
        "count": max_results,
        "search_descriptions": 0,
        "sort_column": "popular",
        "sort_dir": "desc",
        "appid": DOTA_2_APP_ID,
        "norender": 1
    }

    try:
        print(f"🔍 Ищем: {search_term}")  # Отладка
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        print(f"📊 Статус ответа: {data.get('success')}")  # Отладка
        print(f"📦 Найдено результатов: {len(data.get('results', []))}")  # Отладка

        results = []
        for item in data.get("results", []):
            results.append({
                "name": item.get("name"),
                "hash_name": item.get("hash_name"),
                "sell_price_text": item.get("sell_price_text"),
                "sell_listings": item.get("sell_listings"),
            })
        
        return results

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка при поиске предметов: {e}")
        return None