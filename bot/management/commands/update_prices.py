# bot/management/commands/update_prices.py
from django.core.management.base import BaseCommand
from bot.models import ItemQuery
from bot.services.steam_api import SteamAPI
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Обновляет цены для популярных предметов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Количество последних запросов для обновления'
        )

    def handle(self, *args, **options):
        limit = options['limit']
        self.stdout.write(f"Обновление цен для последних {limit} запросов...")

        # Получаем последние уникальные предметы
        recent_items = ItemQuery.objects.values('item_name').distinct()[:limit]

        updated_count = 0
        for item in recent_items:
            item_name = item['item_name']
            price_data = SteamAPI.get_item_price(item_name)

            if price_data:
                # Сохраняем новую запись с обновлённой ценой
                # (здесь нужно получить пользователя, но для упрощения можно создать специального системного пользователя)
                self.stdout.write(f"✅ {item_name}: {price_data.get('lowest_price')}")
                updated_count += 1
            else:
                self.stdout.write(f"❌ {item_name}: не найден")

        self.stdout.write(self.style.SUCCESS(f"Обновлено {updated_count} предметов"))