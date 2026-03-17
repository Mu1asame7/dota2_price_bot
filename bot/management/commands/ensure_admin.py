from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os


class Command(BaseCommand):
    help = "Resets superuser password"

    def handle(self, *args, **options):
        # Удаляем старого админа если есть
        User.objects.filter(is_superuser=True).delete()

        # Создаем нового с гарантированным паролем
        username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL", "")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin123")

        User.objects.create_superuser(username, email, password)
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Superuser "{username}" created with password: {password}'
            )
        )
