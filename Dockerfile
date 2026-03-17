# Используем официальный образ Python
FROM python:3.12-slim

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Копируем файл с зависимостями и устанавливаем их.
#    Копирование только requirements.txt сначала помогает использовать кэш Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем остальной код проекта
COPY . .

# 5. Создаем непривилегированного пользователя для безопасности
RUN adduser --disabled-password --gecos "" appuser

# 6. Меняем владельца файлов на созданного пользователя
RUN chown -R appuser:appuser /app

# 7. Переключаемся на обычного пользователя
USER appuser

# 8. Команда для запуска приложения
#    Используем PORT из окружения Render или 10000 по умолчанию
CMD gunicorn dota2_bot_project.wsgi:application --bind 0.0.0.0:${PORT:-10000}