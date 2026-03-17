# bot/bot.py
import logging
import re
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from asgiref.sync import sync_to_async

from bot.services.steam_api import SteamAPI
from bot.models import TelegramUser, ItemQuery

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user

    # Создаем асинхронную обертку для get_or_create
    get_or_create_user = sync_to_async(TelegramUser.objects.get_or_create)

    # Вызываем асинхронно
    telegram_user, created = await get_or_create_user(
        user_id=user.id,
        defaults={
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
    )

    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n\n"
        f"Я бот для отслеживания цен предметов Dota 2.\n"
        f"Отправь мне название предмета, и я покажу его текущую цену в Steam.\n\n"
        f"Пример: 'Arcana of the Fiend' или 'Pudge Arcana'"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    await update.message.reply_text(
        "ℹ️ Доступные команды:\n"
        "/start - Начало работы\n"
        "/help - Показать это сообщение\n\n"
        "Просто отправь мне название предмета, например: 'Pudge Arcana'"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений (названий предметов)"""
    user = update.effective_user
    message_text = update.message.text.strip()

    await update.message.reply_text(f"🔍 Ищу информацию о '{message_text}'...")

    try:
        # Асинхронно получаем пользователя
        get_user = sync_to_async(TelegramUser.objects.get)
        telegram_user = await get_user(user_id=user.id)

        # Синхронно получаем данные из Steam API (это нормально)
        price_data = SteamAPI.get_item_price(message_text)

        # Асинхронно сохраняем запрос
        create_query = sync_to_async(ItemQuery.objects.create)
        await create_query(
            user=telegram_user, item_name=message_text, price_data=price_data
        )

        if price_data:
            response = (
                f"✅ **{price_data['name']}**\n\n"
                f"💰 Текущая цена: {price_data.get('lowest_price', 'Неизвестно')}\n"
                f"📊 Средняя цена: {price_data.get('median_price', 'Неизвестно')}\n"
                f"📦 Объём продаж: {price_data.get('volume', 'Неизвестно')}\n\n"
                f"#Dota2 #Steam"
            )
        else:
            search_results = SteamAPI.search_items(message_text, max_results=5)

            if search_results:
                response = f"❌ Предмет '{message_text}' не найден.\n\n"
                response += "🔍 Похожие предметы:\n"
                for item in search_results:
                    response += f"• {item['name']} - {item.get('sell_price_text', 'Цена не указана')}\n"
                response += "\nПопробуйте уточнить название."
            else:
                response = f"❌ Предмет '{message_text}' не найден. Попробуйте другое название."

        await update.message.reply_text(response, parse_mode="Markdown")

    except TelegramUser.DoesNotExist:
        await update.message.reply_text(
            "Пожалуйста, сначала введите /start для регистрации."
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await update.message.reply_text(
            "😔 Произошла ошибка при обработке запроса. Попробуйте позже."
        )


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /profile"""
    user = update.effective_user
    try:
        get_user = sync_to_async(TelegramUser.objects.get)
        telegram_user = await get_user(user_id=user.id)

        total_queries = await sync_to_async(
            ItemQuery.objects.filter(user=telegram_user).count
        )()

        await update.message.reply_text(f"📊 Всего запросов: {total_queries}")

    except TelegramUser.DoesNotExist:
        await update.message.reply_text(
            "Пожалуйста, сначала введите /start для регистрации."
        )


def main():
    """Запуск бота"""
    import os
    from dotenv import load_dotenv

    load_dotenv()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN не найден в .env файле")
        return

    # Настраиваем Django (нужно для работы с моделями)
    import django

    django.setup()

    # Создаём приложение
    application = Application.builder().token(token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )
    application.add_handler(CommandHandler("profile", profile_command))

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
