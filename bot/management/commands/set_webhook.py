import asyncio
from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot


class Command(BaseCommand):
    help = "Устанавливает вебхук для Telegram бота"

    def add_arguments(self, parser):
        parser.add_argument(
            "webhook_url",
            type=str,
            help="Базовый URL вашего приложения (например, https://your-app.onrender.com)",
        )

    def handle(self, *args, **options):
        webhook_url = options["webhook_url"]
        # Добавляем /webhook/ к URL
        full_webhook_url = f"{webhook_url.rstrip('/')}/webhook/"

        self.stdout.write(f"Устанавливаю вебхук на {full_webhook_url}...")
        asyncio.run(self.set_webhook(full_webhook_url))

    async def set_webhook(self, webhook_url):
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        try:
            # Удаляем старый вебхук на всякий случай
            await bot.delete_webhook()

            # Устанавливаем новый
            result = await bot.set_webhook(
                url=webhook_url,
                allowed_updates=["message"],  # Можно указать типы обновлений
            )

            if result:
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Вебхук успешно установлен на {webhook_url}")
                )

                # Проверяем информацию о вебхуке
                webhook_info = await bot.get_webhook_info()
                self.stdout.write(f"Информация о вебхуке: {webhook_info}")
            else:
                self.stdout.write(self.style.ERROR("❌ Не удалось установить вебхук"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
        finally:
            await bot.session.close()
