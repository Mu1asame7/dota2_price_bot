from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    """Модель для хранения информации о пользователях Telegram"""
    user_id = models.BigIntegerField(unique=True, verbose_name="ID пользователя")
    username = models.CharField(max_length=255, blank=True, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Фамилия")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Пользователь Telegram"
        verbose_name_plural = "Пользователи Telegram"

    def __str__(self):
        return f"{self.username or self.user_id}"


class ItemQuery(models.Model):
    """Модель для хранения запросов о предметах"""
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='queries')
    item_name = models.CharField(max_length=512, verbose_name="Название предмета")
    price_data = models.JSONField(blank=True, null=True, verbose_name="Данные о цене")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время запроса")

    class Meta:
        verbose_name = "Запрос предмета"
        verbose_name_plural = "Запросы предметов"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.item_name} @ {self.created_at}"