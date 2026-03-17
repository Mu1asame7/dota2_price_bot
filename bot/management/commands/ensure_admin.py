from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates a superuser if none exists'

    def handle(self, *args, **options):
        # Проверяем, есть ли уже суперпользователь
        if not User.objects.filter(is_superuser=True).exists():
            # Берем данные из переменных окружения или ставим значения по умолчанию
            username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
            email = os.getenv('DJANGO_SUPERUSER_EMAIL', '')
            password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin123')
            
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'✅ Superuser "{username}" created successfully'))
        else:
            self.stdout.write('✅ Superuser already exists')