import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import asyncio

# Импортируем твои обработчики из bot.py
from bot.bot import start_command, help_command, handle_message

logger = logging.getLogger(__name__)

# Создаем приложение один раз при загрузке модуля
application = None


async def get_application():
    """Создает или возвращает существующее приложение (асинхронно)"""
    global application
    if application is None:
        print("⚙️ Создаю новое приложение Telegram")
        builder = Application.builder().token(settings.TELEGRAM_BOT_TOKEN)
        application = builder.build()

        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
        )

        # 👇 ВАЖНО: await перед асинхронным методом!
        await application.initialize()

        print("✅ Telegram application initialized")
    return application


@csrf_exempt
def telegram_webhook(request):
    """Обработчик вебхука от Telegram"""
    if request.method == "POST":
        try:
            # Получаем JSON от Telegram
            json_str = request.body.decode("UTF-8")
            logger.debug(f"Received webhook data: {json_str[:200]}...")

            # Создаем новый event loop для асинхронного вызова
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Асинхронно получаем application и обрабатываем update
            app = loop.run_until_complete(get_application())
            update = Update.de_json(json.loads(json_str), app.bot)
            loop.run_until_complete(app.process_update(update))

            # Telegram ожидает ответ "OK"
            return HttpResponse("OK")

        except Exception as e:
            logger.error(f"Error processing webhook: {e}", exc_info=True)
            return JsonResponse({"error": str(e)}, status=500)

    # GET запрос — просто показываем статус
    return JsonResponse(
        {
            "status": "webhook active",
            "message": "Send POST requests here for Telegram updates",
        }
    )
