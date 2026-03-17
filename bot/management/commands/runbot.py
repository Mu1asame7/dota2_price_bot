# bot/management/commands/runbot.py
from django.core.management.base import BaseCommand
from bot.bot import main


class Command(BaseCommand):
    help = 'Запускает Telegram бота'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Запуск Telegram бота...'))
        main()